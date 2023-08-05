
subroutine get_remap_pix_len(x1min, x1max, grid1, x2min, x2max, grid2, pixlen)
  ! Find pixel weight length.
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
  !   Number of grid points in grid 2
  !
  ! Returns
  ! -------
  ! pixlen : int
  !   Length of pixel mapping indices and weights.

  implicit none

  ! Parameter declarations

  integer, parameter :: dp = kind(1.d0)

  integer, intent(in) :: grid1, grid2
  real(kind=dp), intent(in) :: x1min, x1max, x2min, x2max

  real(kind=dp) :: boxsize1, boxsize2, dx1, dx2

  integer, intent(out) :: pixlen

  ! Function

  boxsize1 = x1max - x1min
  boxsize2 = x2max - x2min

  dx1 = boxsize1 / real(grid1)
  dx2 = boxsize2 / real(grid2)

  pixlen = int(floor(dx2/dx1)) + 2

end subroutine get_remap_pix_len


subroutine which_pix(xmin, dx, x, pix)

  ! Find pixel along a defined grid.
  !
  ! Parameters
  ! ----------
  ! xmin : float
  !   Minimum along the grid.
  ! dx : float
  !   pixel width.
  ! x : float
  !   A point for which we would like to determine
  !
  ! Returns
  ! -------
  ! pix : int
  !   The pixel the point corresponds to.

  implicit none

  ! Parameter declarations

  integer, parameter :: dp = kind(1.d0)

  real(kind=dp), intent(in) :: xmin, dx, x
  integer, intent(out) :: pix

  ! Function

  pix = int(floor((x-xmin)/dx))

end subroutine which_pix


subroutine pix1dto2d(xpix, ypix, xlen, ylen, ygrid, pix)

  ! Maps pixels given along a single axis in x and y onto a 2d grid flattened.
  !
  ! Parameters
  ! ----------
  ! xpix : int
  !   Pixel indices along the x axis grid.
  ! ypix : int
  !   Pixel indices along the y axis grid.
  ! xlen : int
  !   Size of the xpix.
  ! ylen : int
  !   Size of the ypix.
  ! ygrid : int
  !   Length of y axis grid.
  !
  ! Returns
  ! -------
  ! pix : int
  !   2d grid pixel.

  implicit none

  integer, intent(in) :: xlen, ylen, ygrid
  integer, intent(in) :: xpix(xlen), ypix(ylen)
  integer, intent(out) :: pix(xlen*ylen)

  integer :: i, j, ii

  ii = 1

  do i = 1, xlen
    do j = 1, ylen
      if ((xpix(i) .NE. -1) .AND. (ypix(j) .NE. -1)) then
        pix(ii) = ypix(j) + ygrid*xpix(i)
      else
        pix(ii) = -1
      end if
      ii = ii + 1
    end do
  end do

end subroutine pix1dto2d


subroutine pix1dto3d(xpix, ypix, zpix, xlen, ylen, zlen, ygrid, zgrid, pix)

  ! Maps pixels given along a single axis in x, y and z onto a 3d grid flattened.
  !
  ! Parameters
  ! ----------
  ! xpix : int
  !   Pixel indices along the x axis grid.
  ! ypix : int
  !   Pixel indices along the y axis grid.
  ! xlen : int
  !   Size of the xpix.
  ! ylen : int
  !   Size of the ypix.
  ! zlen : int
  !   Size of the zpix.
  ! ygrid : int
  !   Length of y axis grid.
  ! zgrid : int
  !   Length of z axis grid.
  !
  ! Returns
  ! -------
  ! pix : int
  !   2d grid pixel.

  implicit none

  integer, intent(in) :: xlen, ylen, zlen, ygrid, zgrid
  integer, intent(in) :: xpix(xlen), ypix(ylen), zpix(zlen)
  integer, intent(out) :: pix(xlen*ylen*zlen)

  integer :: i, j, k, ii

  ii = 1

  do i = 1, xlen
    do j = 1, ylen
      do k = 1, zlen
        if ((xpix(i) .NE. -1) .AND. (ypix(j) .NE. -1) .AND. (zpix(k) .NE. -1)) then
          pix(ii) = zpix(k) + zgrid*(ypix(j) + ygrid*xpix(i))
        else
          pix(ii) = -1
        end if
        ii = ii + 1
      end do
    end do
  end do

end subroutine pix1dto3d


subroutine remap_1d_grid2grid_pixel(x1min, x1max, grid1, x2min, x2max, grid2, which2pix, pixlen, pix, weights)

  ! Computes the exact weights for mapping a single pixel from a new grid (denoted by 2) onto an initial grid
  ! (denoted with 1).
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
  ! which2pix : int
  !   Pixel in grid 2.
  ! pixlen : int
  !   Length of pixel mapping indices and weights.
  !
  ! Returns
  ! -------
  ! pix : int
  !   Pixels to map 2 to 1.
  ! weights : floats
  !   Weights to map 2 to 1.

  implicit none

  ! Parameter declarations

  integer, parameter :: dp = kind(1.d0)

  integer, intent(in) :: grid1, grid2, which2pix, pixlen
  real(kind=dp), intent(in) :: x1min, x1max, x2min, x2max
  integer, intent(out) :: pix(pixlen)
  real(kind=dp), intent(out) :: weights(pixlen)

  real(kind=dp) :: boxsize1, boxsize2, dx1, dx2, x1edge1, x1edge2, x2edge1, x2edge2
  integer :: i, pix1, pix2

  ! Function

  boxsize1 = x1max - x1min
  boxsize2 = x2max - x2min

  dx1 = boxsize1 / real(grid1)
  dx2 = boxsize2 / real(grid2)

  x2edge1 = x2min + dx2*real(which2pix)
  x2edge2 = x2min + dx2*real(which2pix+1)

  call which_pix(x1min, dx1, x2edge1, pix1)
  call which_pix(x1min, dx1, x2edge2, pix2)

  if (pix1 .NE. pix2) then
    do i = 1, pixlen
      pix(i) = pix1 + i-1
      if ((pix(i) .GE. 0) .AND. (pix(i) .LT. grid1)) then
        x1edge1 = x1min + dx1*real(pix(i))
        x1edge2 = x1min + dx1*real(pix(i)+1)
        if ((x2edge1 .GE. x1edge1) .AND. (x2edge2 .LE. x1edge2)) then
          weights(i) = (x2edge2 - x2edge1)/(x2edge2 - x2edge1)
        else if ((x2edge1 .LT. x1edge1) .AND. (x2edge2 .LE. x1edge2) .AND. (x2edge2 .GT. x1edge1)) then
          weights(i) = (x2edge2 - x1edge1)/(x2edge2 - x2edge1)
        else if ((x2edge1 .GE. x1edge1) .AND. (x2edge1 .LT. x1edge2) .AND. (x2edge2 .GT. x1edge2)) then
          weights(i) = (x1edge2 - x2edge1)/(x2edge2 - x2edge1)
        else if ((x2edge1 .LT. x1edge1) .AND. (x2edge2 .GT. x1edge2)) then
          weights(i) = (x1edge2 - x1edge1)/(x2edge2 - x2edge1)
        else
          weights(i) = 0.
          pix(i) = -1
        end if
      else
        weights(i) = 0.
        pix(i) = -1
      end if

    end do
  else if (pix1 .NE. -1) then
    do i = 1, pixlen
      pix(i) = pix1 + i-1
      if ((pix(i) .GE. 0) .AND. (pix(i) .LT. grid1)) then
        if (i .EQ. 1) then
          weights(i) = 1.
        else
          weights(i) = 0.
        end if
      else
        weights(i) = 0.
        pix(i) = -1
      end if
    end do
  end if

end subroutine remap_1d_grid2grid_pixel
