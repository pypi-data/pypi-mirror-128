include "remap_utils.f90"


subroutine remap_1d_grid2grid(x1min, x1max, grid1, x2min, x2max, grid2, pixlen, f1, f2)

  ! Remaps field 1 onto field 2 using exact weights.
  !
  ! Parameters
  ! ----------
  ! x1min : float
  !   Minimum in grid 1.
  ! x1max : float
  !   Maximum in grid 1.
  ! grid1 : int
  !   Number of grid points in grid 1.
  ! x2min : float
  !   Minimum in grid 2.
  ! x2max : float
  !   Maximum in grid 2.
  ! grid2 : int
  !   Number of grid points in grid 2.
  ! pixlen : int
  !   Length of pixel mapping indices and weights.
  ! f1 : array
  !   Values on grid 1.
  !
  ! Returns
  ! -------
  ! f2 : array
  !   Remapped field 1 onto field 2.

  implicit none

  ! Parameter declarations

  integer, parameter :: dp = kind(1.d0)

  integer, intent(in) :: grid1, grid2, pixlen
  real(kind=dp), intent(in) :: x1min, x1max, x2min, x2max, f1(grid1)
  real(kind=dp), intent(out) :: f2(grid2)
  real(kind=dp) :: weights(pixlen)
  integer :: pix(pixlen), i, j, which2pix

  ! Function

  do i = 1, grid2

    which2pix = i-1

    call remap_1d_grid2grid_pixel(x1min, x1max, grid1, x2min, x2max, grid2, which2pix, pixlen, pix, weights)

    f2(i) = 0.

    do j = 1, pixlen

      if (pix(j) .ne. -1) then
        f2(i) = f2(i) + weights(j)*f1(pix(j)+1)
      end if

    end do

  end do

end subroutine remap_1d_grid2grid
