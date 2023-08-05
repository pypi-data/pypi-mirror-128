include "remap_1d_grid2grid.f90"


subroutine remap_3d_grid2grid(x1min, x1max, x1grid, y1min, y1max, y1grid, z1min, z1max, z1grid &
  , x2min, x2max, x2grid, y2min, y2max, y2grid, z2min, z2max, z2grid, xpixlen, ypixlen, zpixlen, f1, f2)

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
  ! z1min : float
  !   Minimum z in grid 1.
  ! z1max : float
  !   Maximum z in grid 1.
  ! z1grid : int
  !   Number of grid points in grid 1 along z.
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
  ! z2min : float
  !   Minimum z in grid 2.
  ! z2max : float
  !   Maximum z in grid 2.
  ! z2grid : int
  !   Number of grid points in grid 2 along z.
  ! xpixlen : int
  !   Length of pixel mapping indices and weights along x.
  ! ypixlen : int
  !   Length of pixel mapping indices and weights along y.
  ! zpixlen : int
  !   Length of pixel mapping indices and weights along z.
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

  integer, intent(in) :: x1grid, y1grid, z1grid, x2grid, y2grid, z2grid, xpixlen, ypixlen, zpixlen
  real(kind=dp), intent(in) :: x1min, x1max, x2min, x2max
  real(kind=dp), intent(in) :: y1min, y1max, y2min, y2max
  real(kind=dp), intent(in) :: z1min, z1max, z2min, z2max
  real(kind=dp), intent(in) :: f1(x1grid*y1grid*z1grid)
  real(kind=dp), intent(out) :: f2(x2grid*y2grid*z2grid)
  real(kind=dp) :: xweights(xpixlen), yweights(ypixlen), zweights(zpixlen)
  integer :: xpix(xpixlen), ypix(ypixlen), zpix(zpixlen), pix(xpixlen*ypixlen*zpixlen), i, j, k
  integer :: xwhich2pix, ywhich2pix, zwhich2pix, ii, jj, i1, j1, k1

  ! Function

  do i = 1, x2grid

    xwhich2pix = i-1
    call remap_1d_grid2grid_pixel(x1min, x1max, x1grid, x2min, x2max, x2grid, xwhich2pix, xpixlen, xpix, xweights)

    do j = 1, y2grid

      ywhich2pix = j-1
      call remap_1d_grid2grid_pixel(y1min, y1max, y1grid, y2min, y2max, y2grid, ywhich2pix, ypixlen, ypix, yweights)

      do k = 1, z2grid

        zwhich2pix = k-1
        call remap_1d_grid2grid_pixel(z1min, z1max, z1grid, z2min, z2max, z2grid, zwhich2pix, zpixlen, zpix, zweights)

        call pix1dto3d(xpix, ypix, zpix, xpixlen, ypixlen, zpixlen, y1grid, z1grid, pix)

        ii = zwhich2pix + z2grid*(ywhich2pix + y2grid*xwhich2pix) + 1
        f2(ii) = 0.

        jj = 1

        do i1 = 1, xpixlen
          do j1 = 1, ypixlen
            do k1 = 1, zpixlen

              if (pix(jj) .NE. -1) then
                f2(ii) = f2(ii) + xweights(i1)*yweights(j1)*zweights(k1)*f1(pix(jj)+1)
              end if

              jj = jj + 1

            end do
          end do
        end do

      end do
    end do
  end do

end subroutine remap_3d_grid2grid
