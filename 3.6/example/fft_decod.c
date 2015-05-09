// gcc -lm -lfftw3

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <math.h>
#include <fftw3.h>

#define MAXSIZE 1000000
#define NSEARCH 260  // 13 periods * 20 pts/period

void remove_avg(unsigned char *d,int *out,int tot_len,int fil_len)
{int tmp,k,avg=0;
 for (k=0;k<fil_len;k++) avg+=d[k];
 for (k=0;k<tot_len-fil_len;k++)
     {out[k]=d[k]-avg/fil_len;
      avg-=d[k];
      avg+=d[k+fil_len];
     }
 for (k=tot_len-fil_len;k<tot_len;k++) out[k]=d[k]-avg/fil_len;
}

int main(int argc,char **argv)
{char filename[255];
 int deb,fin,seuil;
 int k,i,fe=48000,f,N,t,*out,n;
 unsigned char d[MAXSIZE],*toutd,*tout;
 double a=0.;
 int b=0,l0=0;
 fftw_complex *c2400x13,*fc2400x13,*fd,*s,mul,*ss;
 double c2400[20], c1200[20];
 double s2400[20], s1200[20];

 fftw_plan plan_a, plan_b, plan_R;
 double *rs12,*rs24,*rc12,*rc24;

 if (argc<5) printf("%s filename deb fin seuil\n",argv[0]); else
   {sprintf(filename,"%s",argv[1]);
    deb=atoi(argv[2]);
    fin=atoi(argv[3]);
    seuil=atoi(argv[4]);
   }
 if ((fin-deb)>MAXSIZE) 
    {fin=deb+MAXSIZE;
     fprintf(stderr,"deb=%d fin=%d\n",deb,fin);
    }
 f=open(filename,O_RDONLY);
 if (f<0) fprintf(stderr,"open error %d\n",f);
 k=lseek(f,deb,SEEK_SET);
 if (k!=deb) fprintf(stderr,"lseek error %d\n",k);
 N=read(f,d,fin-deb);      // d=d(deb:fin); N=fin-deb;
 close (f);           //    % retranche moyenne glissante sur 3 periodes
 out=(int*)malloc(sizeof(int)*N);
 remove_avg(d,out,N,60);  // c=ones(60,1)/60; dm=conv(d,c);dm=dm(60/2:end-60/2); d=d-dm;

 c2400x13 = (fftw_complex *) fftw_malloc (sizeof (fftw_complex) * N);
 fc2400x13= (fftw_complex *) fftw_malloc (sizeof (fftw_complex) * N);
 fd       = (fftw_complex *) fftw_malloc (sizeof (fftw_complex) * N);
 s        = (fftw_complex *) fftw_malloc (sizeof (fftw_complex) * N);
 ss       = (fftw_complex *) fftw_malloc (sizeof (fftw_complex) * N);
 for (t=0;t<520;t++)  // t=[0:520]; c2400x13=exp(i*t*2400/fe*2*pi);
    {c2400x13[t][0]=cos((double)t*2400./fe*2*M_PI);
     c2400x13[t][1]=sin((double)t*2400./fe*2*M_PI);
    }
 for (t=520;t<N;t++) {c2400x13[t][0]=0;c2400x13[t][1]=0;}
 for (k=0;k<N;k++) {s[k][0]=(double)out[k];s[k][1]=0.;}
 plan_a=fftw_plan_dft_1d(N, c2400x13, fc2400x13, FFTW_FORWARD, FFTW_ESTIMATE);
 plan_b=fftw_plan_dft_1d(N, s, fd , FFTW_FORWARD, FFTW_ESTIMATE);
 plan_R=fftw_plan_dft_1d(N, fd,ss, FFTW_BACKWARD, FFTW_ESTIMATE);
 fftw_execute (plan_a);
 fftw_execute (plan_b);
 for (k=0;k<N;k++) 
    {mul[0]=fc2400x13[k][0]*fd[k][0]-fc2400x13[k][1]*fd[k][1];
     mul[1]=fc2400x13[k][1]*fd[k][0]+fc2400x13[k][0]*fd[k][1];
     fd[k][0]=mul[0]/(float)N;
     fd[k][1]=mul[1]/(float)N;
    }
 fftw_execute (plan_R);
 fftw_destroy_plan (plan_a);
 fftw_destroy_plan (plan_b);
 fftw_destroy_plan (plan_R); // s=conv(c2400x13,d);
 for (k=0;k<N-NSEARCH;k++) if (ss[k+NSEARCH-2][0]>a) {a=ss[k+NSEARCH-2][0];b=k;} // [a,b]=max(real(s)); 
 printf("a=%f b=%d\n",a,b);
 // % plot(d(b-260:b+260)/120,'g');hold on; plot(real(c2400x13),'r');
 b=b%20; // ajout du -5 car on est cal'es sur cos, et on veut sin (passage a 0)
         // b=mod(b,20);    % revient au debut par pas de 2pi
         // d=d(b+400:end); % bien se caler est fondamental pour la suite 
         //                 % est-il judicieux d'essayer a +/-1 ?


 for (t=0;t<20;t++)  // t=[0:520]; c2400x13=exp(i*t*2400/fe*2*pi);
    {c2400[t]=cos((double)t*2400./fe*2*M_PI); //  t=[0:20];  % 2400 Hz dans 48 kHz = 20 points/periode 
     s2400[t]=sin((double)t*2400./fe*2*M_PI); //  c2400=exp(i*t*2400/fe*2*pi);
     c1200[t]=cos((double)t*1200./fe*2*M_PI); //  c1200=exp(i*t*1200/fe*2*pi);
     s1200[t]=sin((double)t*1200./fe*2*M_PI);
    }
 
 rs12=(double*)malloc(sizeof(double)*(N-b)/20); // fin20=floor(length(s12)/20)*20;
 rs24=(double*)malloc(sizeof(double)*(N-b)/20); // s12=s12(1:fin20);s24=s24(1:fin20);
 rc12=(double*)malloc(sizeof(double)*(N-b)/20); // fin20=floor(length(s12)/20)*20;
 rc24=(double*)malloc(sizeof(double)*(N-b)/20); // s12=s12(1:fin20);s24=s24(1:fin20);
 l0=0;
 for (k=b;k<N-20;k+=20)
    {rs12[l0]=0.; rs24[l0]=0.; rc12[l0]=0.; rc24[l0]=0.;
     for (t=0;t<20;t++)
       {rs24[l0]+=((double)out[k+t]*s2400[t]);
        rc24[l0]+=((double)out[k+t]*c2400[t]);
        rs12[l0]+=((double)out[k+t]*s1200[t]);
        rc12[l0]+=((double)out[k+t]*c1200[t]);
       }
    rs12[l0]=sqrt(rs12[l0]*rs12[l0]+rc12[l0]*rc12[l0]);
    rs24[l0]=sqrt(rs24[l0]*rs24[l0]+rc24[l0]*rc24[l0]);
    l0++;
    }

 l0=0;
 do l0++; while ((rs24[l0]+rs12[l0])<2*seuil);  // cherche debut
 do l0++; while ((rs24[l0]+rs12[l0])>2*seuil);  // cherche fin
 fin=l0; 

 l0=0; 
 do l0++; while (rs24[l0]<seuil);   // ll=find(rs24>seuil);ll=ll(1);rs12=rs12(ll:end);rs24=rs24(ll:end);
 do l0++; while (rs12[l0]<rs24[l0]);   // l=find(rs12>rs24);l=l(1);rs12=rs12(l:end);rs24=rs24(l:end);
 toutd=(char*)malloc(fin-l0);
 tout=(char*)malloc(fin-l0+2);
 for (k=l0;k<fin;k++)  // pos12=find(rs12>rs24);pos24=find(rs24>rs12);toutd(pos12)=0;toutd(pos24)=1;
     {if (rs24[k]>rs12[k]) toutd[k-l0]=1; else toutd[k-l0]=0;
     }

  n=0;
  tout[n]=1;n++;tout[n]=1;n++; // les deux premiers 1 sont oublie's car on se sync sur 1200
  for (k=0;k<fin-l0;k++)
    {if (toutd[k]==0) tout[n]=1-tout[n-1]; else tout[n]=tout[n-1];
     n=n+1;
    }
  for (k=0;k<fin-l0;k+=8) printf("%02x ",tout[k]+tout[k+1]*2+tout[k+2]*4+tout[k+3]*8+tout[k+4]*16+tout[k+5]*32+tout[k+6]*64);
  printf("\n");
  for (k=0;k<fin-l0;k+=8) printf("%c",   tout[k]+tout[k+1]*2+tout[k+2]*4+tout[k+3]*8+tout[k+4]*16+tout[k+5]*32+tout[k+6]*64);
}
// checksomme=1-mod(sum(binaire(:,1:7)')',2); % verification
