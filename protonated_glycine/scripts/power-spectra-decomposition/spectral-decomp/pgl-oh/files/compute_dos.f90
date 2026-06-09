!==============================================================================
!
! Compute infrared spectrum from classical correlation function
!
!==============================================================================

program compute_quantum_spectrum

   implicit none

   real(8), parameter :: conv_time = 1.d-12
   real(8), parameter :: conv_length = 1.d-10
   real(8), parameter :: conv_freq = 2.99792d10
   real(8), parameter :: hplanck = 6.62606876d-34
   real(8), parameter :: hbar = 1.054571596d-34
   real(8), parameter :: kboltz = 1.3806503d-23
   real(8), parameter :: epsilon_vacuum = 8.8541878d-12
   real(8), parameter :: light_velocity = 2.99792d8

   !....................................................

   integer :: Ntime, Ndata, Nskip, nav

   real(8) :: pi
   real(8) :: box_length, volume, time_integration, alpha
   real(8) :: arg, arg1
   real(8) :: delta_time, delta_nu, omega
   real(8) :: temp, kT, beta, beta_hplanck_nu, nu_time
   real(8) :: factor_centroid, factor_quantum, normalization

   real(8), allocatable :: time(:), nu(:)
   real(8), allocatable :: corr_tot(:)
   real(8), allocatable :: spectrum(:)
   real(8), allocatable :: spectrum_centroid(:)
   real(8), allocatable :: spectrum_quantum(:)

   !....................................................

   integer :: itime, inu, icount, ncount, i, iav

   real(8) :: tmp, tmp1, intensity, intensity1, intensity2
   real(8) :: omega_tmp(100), intensity_tmp(100), omega_av, intensity_av

   !....................................................

   namelist/ input / Ntime, temp, volume, time_integration, Nskip, ncount, nav, alpha

   !....................................................

   open(unit=1, file='input_dos')
   open(unit=101, file='corr_vel.res')

   open(unit=201, file='dos_centroid.res')
   open(unit=202, file='dos_quantum.res')
   open(unit=203, file='dos_quantum_smooth.res')

   !....................................................

   read(1,nml=input)

   volume = volume*conv_length**3

   !______________________________

   allocate(time(-Ntime:Ntime))
   allocate(corr_tot(-Ntime:Ntime))
   allocate(nu(-Ntime:Ntime))
   allocate(spectrum(-Ntime:Ntime))
   allocate(spectrum_centroid(-Ntime:Ntime))
   allocate(spectrum_quantum(-Ntime:Ntime))

   !______________________________

!! Initialize arrays.

   corr_tot(:) = 0.d0
   spectrum(:) = 0.d0
   spectrum_centroid(:) = 0.d0
   spectrum_quantum(:) = 0.d0

   !______________________________

!! Read data.

   do itime = 0, Ntime

      read(101,*) time(itime), corr_tot(itime)

      corr_tot(itime) = corr_tot(itime) * exp(-alpha**2 * time(itime)**2)

      if (itime .gt. 0) then
         time(-itime) = time(itime)
         corr_tot(-itime) = corr_tot(itime)
      end if

      if (time(itime) .eq. time_integration) exit

   end do

   Ndata = itime

   print*, "Ndata = ", Ndata

   corr_tot(Ndata) = 0.d0
   corr_tot(-Ndata) = 0.d0

   !______________________________

!! Set paramters.

   pi = acos(-1.d0)

   arg = 2.d0 * pi / dble(2 * Ndata - 1)

   kT = kboltz * temp

   beta = 1.d0 / kT

   normalization = 3.d0 * hbar * light_velocity * volume * epsilon_vacuum
   normalization = 2.d0 * pi / normalization

   !______________________________

!! Set variables.

   ! time step in s
   delta_time = (time(1) - time(0)) * conv_time

   ! frequency step in s-1
   delta_nu = 1.d0 / dble(2 * Ndata - 1) / delta_time

   ! beta * hplanck * delta_omega
   arg1 = beta * hplanck * delta_nu

   !______________________________

!! Infrared spectrum.

   do inu = 0, Ndata, Nskip

      nu(inu) = delta_nu * dble(inu)

      beta_hplanck_nu = arg1 * dble(inu)

      tmp = beta_hplanck_nu / 2.d0

      factor_centroid = nu(inu) * (1.d0 - exp(-beta_hplanck_nu)) / 2.d0
      factor_quantum =  nu(inu) * tmp

      if (inu .eq. 0) factor_quantum = 1.d0

      do itime = -Ndata, Ndata
         nu_time = arg * dble(inu * itime)
         spectrum(inu) = spectrum(inu)  &
            + corr_tot(itime) * cos(nu_time)
      end do

      factor_centroid = factor_centroid * delta_time 
      factor_quantum = factor_quantum * delta_time 

      spectrum_centroid(inu) = spectrum(inu) * factor_centroid
      spectrum_quantum(inu) = spectrum(inu) * factor_quantum

      !! intensity and frequancy in cm-1
      spectrum_centroid(inu) = spectrum_centroid(inu) / 100.d0
      spectrum_quantum(inu) = spectrum_quantum(inu) / 100.d0

      omega = nu(inu) / conv_freq

      write(201,*) omega, spectrum_centroid(inu)
      write(202,*) omega, spectrum_quantum(inu)

   end do


   icount = 0
   iav = 0
   omega = 0.d0
   intensity = 0.d0
   do inu = 0, Ndata, Nskip

      icount = icount + 1

      nu(inu) = delta_nu * dble(inu)
      omega = omega + nu(inu)  
      intensity = intensity + spectrum_quantum(inu)

      if (mod(icount,ncount) .eq. 0) then
         iav = iav + 1
         omega_tmp(iav) = omega / dble(ncount) / conv_freq
         intensity_tmp(iav) = intensity / dble(ncount)
         omega = 0.d0
         intensity = 0.d0
         icount = 0
         if (iav .eq. nav) then
            omega_av = 0.d0
            intensity_av = 0.d0
            do i = 1, nav
               omega_av = omega_av + omega_tmp(i)
               intensity_av = intensity_av + intensity_tmp(i)
            end do
            write(203,*) omega_av / dble(nav), intensity_av / dble(nav)
            iav = 0
         end if
      end if

   end do



end program
