include "remap_1d_grid2grid.f90"


subroutine remap_2d_grid2grid(x1min, x1max, x1grid, y1min, y1max, y1grid &
  , x2min, x2max, x2grid, y2min, y2max, y2grid, xpixlen, ypixlen, f1, f2)

  ! Remaps field 1 onto field 2 using exact weights.
  !
  ! Parameters
  ! ----------
  ! x1min : float
  !   Minimum x in grid 1.
  ! x1max : float
  !   Maximum x in grid 1.
  ! x1grid : int
  !   Number of grid points in grid 1 along x.
  ! y1min : float
  !   Minimum y in grid 1.
  ! y1max : float
  !   Maximum y in grid 1.
  ! y1grid : int
  !   Number of grid points in grid 1 along y.
  ! x2min : float
  !   Minimum x in grid 2.
  ! x2max : float
  !   Maximum x in grid 2.
  ! x2grid : int
  !   Number of grid points in grid 2 along x.
  ! y2min : float
  !   Minimum y in grid 2.
  ! y2max : float
  !   Maximum y in grid 2.
  ! y2grid : int
  !   Number of grid points in grid 2 along y.
  ! xpixlen : int
  !   Length of pixel mapping indices and weights along x.
  ! ypixlen : int
  !   Length of pixel mapping indices and weights along y.
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

  integer, intent(in) :: x1grid, y1grid, x2grid, y2grid, xpixlen, ypixlen
  real(kind=dp), intent(in) :: x1min, x1max, x2min, x2max
  real(kind=dp), intent(in) :: y1min, y1max, y2min, y2max
  real(kind=dp), intent(in) :: f1(x1grid*y1grid)
  real(kind=dp), intent(out) :: f2(x2grid*y2grid)
  real(kind=dp) :: xweights(xpixlen), yweights(ypixlen)
  integer :: xpix(xpixlen), ypix(ypixlen), pix(xpixlen*ypixlen), i, j, xwhich2pix, ywhich2pix, ii, jj, i1, j1

  ! Function

  do i = 1, x2grid

    xwhich2pix = i-1
    call remap_1d_grid2grid_pixel(x1min, x1max, x1grid, x2min, x2max, x2grid, xwhich2pix, xpixlen, xpix, xweights)

    do j = 1, y2grid

      ywhich2pix = j-1
      call remap_1d_grid2grid_pixel(y1min, y1max, y1grid, y2min, y2max, y2grid, ywhich2pix, ypixlen, ypix, yweights)

      call pix1dto2d(xpix, ypix, xpixlen, ypixlen, y1grid, pix)

      ii = ywhich2pix + y2grid*xwhich2pix + 1
      f2(ii) = 0.

      jj = 1

      do i1 = 1, xpixlen
        do j1 = 1, ypixlen

          if (pix(jj) .NE. -1) then
            f2(ii) = f2(ii) + xweights(i1)*yweights(j1)*f1(pix(jj)+1)
          end if

          jj = jj + 1

        end do
      end do

    end do
  end do

end subroutine remap_2d_grid2grid
