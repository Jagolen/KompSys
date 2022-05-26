% Self-propelled particle model of aggregation in two dimensions.
% Written by Kit Yates

clear
close all



%Set up movie
fig=figure;
makemovie=0;
%movien = avifile('Vicsekmovie','FPS',3,'compression','none')

J=100; %Number of timestep t0 be used
UJ=0;   %Rate at which film is updated


t=1/J %Size of one time step

N=60 %Number of particles

e=0.5 %e is eta the noise parameter, whose maximum value is 2*pi

r=1     % radius for where the particles get a common direction
r2=3    % radius where the particles move towards each other



L=20 %L is the size of the domain on which the particles can move

v=0.5 %v is the speed at which the particles move

turn_rate=1; %how hard the particles turn towards biggest groups

% x(i,j) gives the x coordinate of the ith particle at time j
x=zeros(N,J+1);
x(:,1)=L*rand(N,1); %define initial x coordiantes of all particles
     
% y(i,j) gives the y coordinate of the ith particle at time j
y=zeros(N,J+1);
y(:,1)=L*rand(N,1); %define initial y coordiantes of all particles

% T(i,j) gives the angle with the x axis of the direction of motion of the ith
% particle at time j
T=zeros(N,J+1);
T(:,1)=2*pi*rand(N,1); %define initial direction of all particles

D=zeros(N,N); %neigbors of every particle
D_ingroup=zeros(N,N);

closeness = zeros(1,J,'double');
     
%For all time steps
for j=1:J
    %For each particle
    for i=1:N
        %finds how many particles are in the interaction radius of each
        %particle
        A(:,1)=((x(i,j)-x(:,j)).^2+(y(i,j)-y(:,j)).^2).^0.5;
        A(:,2)=((x(i,j)-x(:,j)-L).^2+(y(i,j)-y(:,j)).^2).^0.5;
        A(:,3)=((x(i,j)-x(:,j)).^2+(y(i,j)-y(:,j)-L).^2).^0.5;
        A(:,4)=((x(i,j)-x(:,j)+L).^2+(y(i,j)-y(:,j)).^2).^0.5;
        A(:,5)=((x(i,j)-x(:,j)).^2+(y(i,j)-y(:,j)+L).^2).^0.5;
        A(:,6)=((x(i,j)-x(:,j)+L).^2+(y(i,j)-y(:,j)+L).^2).^0.5;
        A(:,7)=((x(i,j)-x(:,j)+L).^2+(y(i,j)-y(:,j)-L).^2).^0.5;
        A(:,8)=((x(i,j)-x(:,j)-L).^2+(y(i,j)-y(:,j)+L).^2).^0.5;
        A(:,9)=((x(i,j)-x(:,j)-L).^2+(y(i,j)-y(:,j)-L).^2).^0.5;
        
        
        %closeness(j) = sum(min(A,[],2))/N;  %for closeness score
        A_tw = A>1&A<r2;
        A_ingroup = A<3;
        D(i,:) = sum(A_tw')';  % cannot move towards each other if too close
        D_ingroup(i,:) = sum(A_ingroup')';
        A_nb = A<=r;
        B=sum(A_nb')';   

        % gives mean angle of neigbors
        ss=sum(sin(T(:,j)).*B)/sum(B);
        sc=sum(cos(T(:,j)).*B)/sum(B);
        S=atan2(ss,sc);

        T(i,j)=S+e*(rand-0.5); %adds noise to the measured angle
     
    end

    B1=sum(D);  %amount of neigbors for every particle.
    B2=sum(D_ingroup);
    closeness(j)=sum(B2);
    closeness(j)=closeness(j)/(N*N);
    disp(closeness(j));
    for f=1:N
        % find the negbors with most neigbors
        D(f,:) = B1.*D(f,:);
        D(f,f)=0;   %cannot be neigbor with itself
        [~, toward] = max(D(f,:));
        
        % find closest y-path
        possible_sin = [y(toward,j)-y(f,j),...
            y(toward,j)-y(f,j)+L, y(toward,j)-y(f,j)-L];    
        [~, to_index]=min(abs(possible_sin));
        ts=possible_sin(to_index);
        
        % find closest x-path
        possible_cos = [x(toward,j)-x(f,j),...
            x(toward,j)-x(f,j)+L, x(toward,j)-x(f,j)-L];    
        [minn, to_index]=min(abs(possible_cos));
        tc=possible_sin(to_index);
        
        % normalize distances
        S=[ts tc]./(ts^2+tc^2)^0.5*turn_rate;
        % setting new angle that is a mix of the old angle and...
        % the angle towards the neigbor with most neigbors
        T(f,j+1)=atan2(S(1)+sin(T(f,j)),S(2)+cos(T(f,j)))+e*(rand-0.5); %straight towards neighbor with most negbors
        
        
        % Update positions
        x(f,j+1)=x(f,j)+v*cos(T(f,j+1)); %updates the particles' x-coordinates
        y(f,j+1)=y(f,j)+v*sin(T(f,j+1)); %updates the particles' y coordinates
        
        % Jumps from the right of the box to the left or vice versa
        x(f,j+1)=mod(x(f,j+1),L);

        %Jumps from the top of the box to the bottom or vice versa
        y(f,j+1)=mod(y(f,j+1),L);
        

        %Plot particles

        if makemovie
            if abs(x(f,j)-x(f,j+1))<v && abs(y(f,j)-y(f,j+1))<v
                plot([x(f,j), x(f,j+1)] ,[y(f,j),y(f,j+1)],'k-','markersize',4) %plots the first half of the particles in black
                axis([0 L 0 L]);
                hold on
                plot(x(f,j+1) ,y(f,j+1),'k.','markersize',10)
                xlabel('X position')
                ylabel('Y position')
            end
        end
    end
        
        
    
    if makemovie
        hold off
        M(j)=getframe; %makes a movie fram from the plot
        %movien = addframe(movien,M(j)); %adds this movie fram to the movie
    end
 
end

if ~ makemovie
    plot(linspace(0,1,J), closeness)
end

     
%movien = close(movien); %finishes the movie

