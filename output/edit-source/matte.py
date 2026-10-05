import cv2, numpy as np, subprocess, sys, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
W,H=576,1024; OW,OH=1080,1920
seg=vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
  base_options=mpt.BaseOptions(model_asset_path='selfie_mc.tflite'),
  running_mode=vision.RunningMode.VIDEO, output_confidence_masks=True))
def guided(I,p,r,eps):
    m=lambda x: cv2.boxFilter(x,-1,(r,r))
    mI,mp_=m(I),m(p); a=(m(I*p)-mI*mp_)/(m(I*I)-mI*mI+eps); b=mp_-a*mI
    return m(a)*I+m(b)
# wall reference color from top corners of first frame
limit=float(sys.argv[1]) if len(sys.argv)>1 else 1e9
only=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else None
dec=subprocess.Popen(['ffmpeg','-v','error','-i','src.mp4','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
enc=None
if only is None:
  enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{OW}x{OH}','-r','30','-i','-',
   '-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','12M','-crf','18','-row-mt','1','-deadline','good','-cpu-used','2','-auto-alt-ref','0','person.webm'],stdin=subprocess.PIPE)
prev=None; wall=None; i=0
yy,xx=np.mgrid[0:H,0:W]
BAND=((xx<150)|(xx>W-150))&(yy>300)
while True:
  buf=dec.stdout.read(W*H*3)
  if len(buf)<W*H*3 or i>=limit: break
  f=np.frombuffer(buf,np.uint8).reshape(H,W,3)
  rgb=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
  res=seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb),int(i*1000/30))
  cm=[cv2.resize(m.numpy_view().copy(),(W,H),interpolation=cv2.INTER_CUBIC) for m in res.confidence_masks]
  hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
  hh,ss,vv=hsv[...,0],hsv[...,1],hsv[...,2]
  cand=((hh<17)|(hh>170))&(ss<105)&(ss>25)&(vv>55)&(cm[3]<0.3)&(cm[1]<0.3)&BAND
  cand=cv2.morphologyEx(cand.astype(np.uint8),cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
  n,lbl,st,_=cv2.connectedComponentsWithStats(cand,8)
  chair=np.zeros((H,W),np.float32)
  for k in range(1,n):
    x,y,w,h,ar=st[k]
    m=lbl==k
    if ar>1200 and (x<=2 or x+w>=W-2): chair[m]=1

  chair=cv2.dilate(chair,np.ones((13,13),np.uint8))
  chair=cv2.GaussianBlur(chair,(9,9),0)
  skin=cm[2]+cm[3]
  core=np.clip(cm[1]+skin+cm[4],0,1)*(1-chair)
  core=cv2.morphologyEx(core,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
  core=np.maximum(core,cv2.morphologyEx(core,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)))*(1-chair))
  near=cv2.GaussianBlur(cv2.dilate((core>0.5).astype(np.float32),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))),(9,9),0)
  person=np.clip(core+cm[5]*near*0.6*(1-chair),0,1)
  lab=cv2.cvtColor(f,cv2.COLOR_BGR2LAB).astype(np.float32)
  if wall is None:
     wall=np.concatenate([lab[20:120,10:80].reshape(-1,3),lab[20:120,-80:-10].reshape(-1,3)]).mean(0)
  d=np.sqrt(((lab[...,1:]-wall[1:])**2).sum(-1))  # chroma distance from wall
  wallness=np.clip((22-d)/12,0,1)  # 1 = wall colored
  a=np.clip((person-0.42)/0.36,0,1)
  # where the segmenter is unsure, use colour key; kill wall pixels
  a=a*(1-wallness*np.clip(1.2-person,0,1)*1.0)
  a=np.where(wallness>0.85, a*0.0, a)
  gray=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)/255
  a=np.clip(guided(gray,a.astype(np.float32),9,1e-3),0,1)
  if prev is not None: a=np.where(np.abs(a-prev)<0.25,0.6*a+0.4*prev,a)  # temporal smoothing, keep fast motion
  prev=a
  # despill: pull yellow-green tint off edges
  fs=f.astype(np.float32)
  edge=np.clip(1-np.abs(a*2-1),0,1)[...,None]*0.0+ (1-a[...,None])*0.0 + (a[...,None]<0.98)
  b,g,r=fs[...,0],fs[...,1],fs[...,2]
  lim=np.maximum(b,(r+b)/2)
  g2=np.where(g>lim,lim+(g-lim)*0.25,g)
  r2=np.where((r>b+25)&(g>b+25),r-(np.minimum(r,g)-b)*0.12,r)
  fs=np.where(edge>0, np.stack([b,g2,r2],-1), fs)
  out=np.dstack([cv2.cvtColor(np.clip(fs,0,255).astype(np.uint8),cv2.COLOR_BGR2RGB),(a*255).astype(np.uint8)])
  out=cv2.resize(out,(OW,OH),interpolation=cv2.INTER_LANCZOS4)
  if only is not None and i in only:
     cv2.imwrite(f'mt_{i}.png',cv2.cvtColor(out,cv2.COLOR_RGBA2BGRA))
  if enc: enc.stdin.write(out.tobytes())
  i+=1
if enc: enc.stdin.close(); enc.wait()
print('frames',i)
