% f=fopen('120630acars_orleans.wav');
% f=fopen('acars_orleans.wav');
%f=fopen('120630acars_orleans5bon.wav');
%f=fopen('120630acars_orleans4bon.wav');
%f=fopen('120630acars_orleans3.wav');

clear all
close all
more off

seuil=1900 % 7000;

% filename='120630acars_orleans4bon.wav';
% filename='120630acars_orleans3.wav';
filename='120708_besac.wav';
f=fopen(filename);

d=fread(f,inf,'uint8');
fclose(f);
fe=48000

t=[0:520]; % 2400 Hz dans 48 kHz = 20 points/periode *26
c2400x13=exp(i*t*2400/fe*2*pi);

indice=[];
for k=1e4:1e5:length(d)-1e5
  k
  dd=abs(conv(c2400x13,d(k:k+1e5)));
  indices=find(dd>seuil);
  if (length(indices)>0)
    indice=[indice k+indices(1)]    
  end
  indices2=find(diff(indices)>100);
  if (length(indices2)>0)
    indice=[indice k+indices(indices2+1)']; 
  end
end

% plot(d(1181510:10:1181510+1e5),'b');hold on;plot(dd(1:10:end),'r');
if (length(indice)>0)
  for m=1:length(indice)
    indice(m)
    binaire=fft_decod(filename,indice(m)-3000,indice(m)+50000,2000);
  end
end
