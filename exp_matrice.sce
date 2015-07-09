
function Pt=expmat(M,n,C,t)
    Q=[-M-1/C, M, 1/C ; M/(n-1), -M/(n-1), 0 ; 0, 0, 0] //matrice pour T2
    // meme ile , ile differente, coalescence
    Pt=expm(t*Q)
endfunction

pas=0.05 // précision
tmax=10 //fin des temps
n=14 //nb d'iles

T=[0,0.7,9,tmax] //temps de coupure avant tmax
M=[0.11,2.51,0.48] //taux de migration après chaque coupure
C=[59.8,43.76,39.29] //tailles métapop après chaque coupure
//C=[1,0.5,0.5]



i=0

temps=[];Ps=[];fs=[];PT=eye(3)// PT va prendre les Pt figés après le premier temps de coupure
tic()
for cpt=[1:length(T)-1]
    for t=[T(cpt)+pas:pas:T(cpt+1)]
        i=i+1
        temps(i)=t
        Q=PT*expmat(M(cpt),n,C(cpt),t-T(cpt))
        Ps(i)=Q(1,3) // proba que ça coalesce avant t en partant de la même île
        tmp(i)=Q(1,1)
    end
    PT=Q
end

disp(['temps de calcul='])
disp(toc())

for k=1:i-1
    fs(k)=(Ps(k+1)-Ps(k))/(temps(k+1)-temps(k))
    disp(fs(k))
end
fs(i)=fs(i-1)



//IICR=(1-Ps(2:length(Ps)))./fs(2:length(fs))
IICR=(1-Ps)./fs


figure(2)
clf
plot2d(temps,(1-Ps)./fs)
//plot2d('ln',1000*25*temps,1000*IICR)

//plot([0:pas:tmax-pas],fs)


//replot([10000,0,1000*25*tmax,1000*max(IICR)])

//figure(3)
//clf
//plot2d('ln',1000*25*temps,1000*(1-Ps)./tmp)
//replot([10000,0,1000*25*tmax,1000*max(IICR)])



