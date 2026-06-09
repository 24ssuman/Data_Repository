program pbc

  implicit none

  integer, parameter :: Ndim = 3

  character(20) :: atom

  integer :: Natom_tot, Nstep
  integer :: Ntime, itime, dt
  integer :: Nmol, imol
  integer :: Natom, iatom

  real(8) :: box_x_in, box_x_fin
  real(8) :: box_y_in, box_y_fin
  real(8) :: box_z_in, box_z_fin
  real(8), allocatable :: pos(:,:,:)

  namelist/input/Ntime, dt, Nmol, Natom, box_x_in, box_x_fin, box_y_in, box_y_fin, box_z_in, box_z_fin

  open(1,file='input')
  open(unit=3,file='simulation.vel_0.xyz')
  open(unit=11,file='dump.lammpstrj')

  read(1, nml=input)

  allocate( pos(Ndim,Natom,Nmol) )

  do itime = 1, Ntime

     Nstep = dt*(itime-1)

     read(3,*) Natom_tot
     read(3,*)

     write(11,'(a14)') "ITEM: TIMESTEP"
     write(11,*) Nstep

     write(11,'(a21)') "ITEM: NUMBER OF ATOMS"
     write(11,*) Natom_tot

     write(11,'(a25)') "ITEM: BOX BOUNDS ff ff ff"
     write(11,*) box_x_in, box_x_fin
     write(11,*) box_y_in, box_y_fin
     write(11,*) box_z_in, box_z_fin

     write(11,'(a31)') "ITEM: ATOMS id mol type q vx vy vz"

     do imol = 1, Nmol

        do iatom = 1, Natom
           read(3,*) atom, pos(:,iatom,imol)
        end do

        write(11,'(i8,i8,i8,a8,3f15.8)') 1, 1, 1, '0.0000', pos(:,1,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 2, 1, 2, '0.0000', pos(:,2,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 3, 1, 2, '0.0000', pos(:,3,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 4, 1, 2, '0.0000', pos(:,4,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 5, 1, 3, '0.0000', pos(:,5,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 6, 1, 4, '0.0000', pos(:,6,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 7, 1, 4, '0.0000', pos(:,7,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 8, 1, 5, '0.0000', pos(:,8,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 9, 1, 6, '0.0000', pos(:,9,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 10, 1, 7, '0.0000', pos(:,10,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 11, 1, 8, '0.0000', pos(:,11,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 12, 2, 9, '0.0000', pos(:,12,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 13, 2, 10, '0.0000', pos(:,13,imol)
        write(11,'(i8,i8,i8,a8,3f15.8)') 14, 2, 10, '0.0000', pos(:,14,imol)

     end do

  enddo

end program

