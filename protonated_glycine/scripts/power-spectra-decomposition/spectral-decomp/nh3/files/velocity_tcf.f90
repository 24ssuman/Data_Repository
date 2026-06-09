!==============================================================================
 
program velocity_tcf

   implicit none

   integer, parameter :: Ndim = 3
   real(8), parameter :: conv_length = 1.d-10  !! Angstrom to meter

   !.......................................................

   character(10) :: atom_name

   integer :: Nmof, Nmol, Natom, Ntime_tot, Ntime
   integer :: Nmol1, Nmol2, Natom1, Natom2

   real(8) :: dt, time, time_max
   real(8), allocatable :: Nav(:)

   !.......................................................

   real(8), allocatable :: vel_tot(:,:), vel(:,:,:)

   real(8) :: corr_vel_tot
   real(8), allocatable :: corr_vel(:,:)

   !.......................................................

   integer :: idim, iatom, imol, imof, itime

   integer :: itime1, itime2, jmol

   namelist/input/dt, Nmof, Nmol, Nmol1, Nmol2, Natom, Natom1, Natom2, time_max

   !.......................................................

   open(unit=1, file='input_vel')
   open(unit=2, file='NTIME')
   open(unit=11, file='VELOCITY_CMD')

   !.......................................................

   open(unit=101, file='corr_vel.res' )

   !.......................................................

   read(1,nml=input)

   read(2,*) Ntime_tot
   Ntime_tot = Ntime_tot - 1

   !Ntime = int(time_max / dt) + 1
   Ntime = Ntime_tot

   !__________________________________________

   !! Allocate arrays.

   allocate(Nav(0:Ntime_tot))

   allocate(vel(Ndim,Natom,Nmol))

   allocate(vel_tot(Ndim,0:Ntime_tot))

   allocate(corr_vel(Ndim,0:Ntime_tot))

   !__________________________________________

   !! Read trajectory.

   vel_tot(:,:) = 0.d0

   do itime = 0, Ntime_tot

      read(11,*)

      do imof = 1, Nmof
         read(11,*)
      end do

      do imol = 1, Nmol

         do iatom = 1, Natom

            read(11,*) atom_name, vel(:,iatom,imol)

            if ((imol.ge.Nmol1 .and. imol.le.Nmol2) .and. (iatom.ge.Natom1 .and. iatom.le.Natom2)) then

               vel_tot(:,itime) = vel_tot(:,itime) + vel(:,iatom,imol)

            end if

         end do

      enddo

   end do

   !__________________________________________

   !! Compute autocorrelation function.

   Nav(:) = 0
   corr_vel(:,:) = 0.d0

   do itime1 = 0, Ntime_tot

      do itime2 = itime1, Ntime_tot

         itime = itime2 - itime1

         if (itime .gt. Ntime) cycle

         Nav(itime) = Nav(itime) + 1

         do idim = 1, Ndim
            corr_vel(idim,itime) = corr_vel(idim,itime)  &
                + vel_tot(idim,itime2) * vel_tot(idim,itime1)
         end do

      end do

   end do

   !__________________________________________

   !! Print tcf.

   do itime = 0, Ntime
      
      time = dt * dble(itime)
      corr_vel_tot = 0.d0
     
      do idim = 1, Ndim
         corr_vel_tot =  corr_vel_tot & 
            + corr_vel(idim,itime) / dble( Nav(itime) )
      end do
      
      write(101,*) time, corr_vel_tot

   end do

end program

