function binaire=fft_decod(filename,deb,fin,seuil)

jmfdebug=0;

fe=48000;
%deb=  indice  ;
%fin=  indice+23000 ;

  f=fopen(filename);
  d=fread(f,inf,'uint8');

  d=d(deb:fin);
  N=fin-deb;
  
  c=ones(60,1)/60;
  dm=conv(d,c);dm=dm(60/2:end-60/2);
  d=d-dm;   % remove sliding average over 3 periods

  t=[0:519]; % 2400 Hz in 48 kHz = 20 points/period *26
  c2400x13=exp(i*t*2400/fe*2*pi);
  
% searchs for max of 13 periods at 2400 Hz 
  s=conv(c2400x13,d);
  s=s(length(t)/2:end-length(t)/2);
  [a,b]=max(real(s));   % cross-correlation maximum in b
  % plot(d(b-260:b+260)/120,'g');hold on; plot(real(c2400x13),'r');

b
  b=mod(b,20)+5;    % back to beginning using 2pi steps
b
  d=d(b+400:end); % being correctly positioned is fundamental for the decoding
                  % would it be worth trying +/-1 ?

  t=[0:19];  % 2400 Hz in 48 kHz = 20 points/period
  c2400=exp(i*t*2400/fe*2*pi);
  c1200=exp(i*t*1200/fe*2*pi);
  s12=conv(c1200,d);
  s24=conv(c2400,d);
  %  plot(d); hold on;plot(real(s12),'r'); plot(real(s24),'r');
  fin20=floor(length(s12)/20)*20;
  s12=s12(1:fin20);s24=s24(1:fin20);
  rs12=reshape(abs(s12),20,length(s12)/20);
  rs24=reshape(abs(s24),20,length(s24)/20);
  rs12=sum(rs12);  
  if (jmfdebug==1) 
     plot(rs12,'bo-');end
  rs24=sum(rs24);  
  if (jmfdebug==1) 
     hold on;plot(rs24,'ro-');legend('1200','2400');end
 
seuil=max(rs24)*0.55; 
  l0=find((rs24+rs12)>seuil);   % only keep useful samples
  rs12=rs12(l0);rs24=rs24(l0);
   
  ll=find(rs24>seuil);ll=ll(1)
  rs12=rs12(ll:end);
  rs24=rs24(ll:end);
  l=find(rs12>rs24);l=l(1)
  rs12=rs12(l:end);
  rs24=rs24(l:end);

  pos12=find(rs12>rs24);
  pos24=find(rs24>rs12);
  if (jmfdebug ==1) 
     plot(pos12+l+ll+l0(1),max(rs24)+5,'go'); hold on
     plot(pos24+l+ll+l0(1),max(rs24)+10,'mo');
  end
  toutd(pos12)=0;
  toutd(pos24)=1;

  n=1;
  tout(n)=1;n=n+1;  % the first two '1' are forgotten since we sync on 1200 Hz
  tout(n)=1;n=n+1;
  for k=1:length(toutd)  % integral ?
    if (toutd(k)==0)
       tout(n)=1-tout(n-1); else tout(n)=tout(n-1);
    endif
    n=n+1;
  end

  binaire=reshape(tout(1:floor(length(tout)/8)*8),8,floor(length(tout)/8))';
  code_asc=binaire(:,1)+binaire(:,2)*2+binaire(:,3)*4+binaire(:,4)*8+binaire(:,5)*16+binaire(:,6)*32+binaire(:,7)*64;
  checksomme=1-mod(sum(binaire(:,1:7)')',2); % verification
 
  if (code_asc(1)==0x2b) && (code_asc(2)==0x2a)
    printf('%02x ',code_asc); printf('\n');
    printf('%c',   code_asc); printf('\nCRC:'); printf('%d',checksomme-binaire(:,8)); printf('\n');
  else
    printf("The sequence must start with 2B 2A 16 16 01 -> %02x %02x\n",code_asc(1), code_asc(2));
  end
