    .data
array:      .word 10, 3, 7, 2, 8, 6, 1, 9, 5, 4
arr_len:    .word 10

    .text
    .globl _start

_start:
    la s0, array        # s0 = base address of array
    lw s1, arr_len      # s1 = array length
    addi s2, zero, 0    # s2 = low index
    addi s3, s1, -1     # s3 = high index
    call quicksort

exit:
    # Infinite loop (halt)
    j exit

# void quicksort(int* arr, int low, int high)
quicksort:
    addi sp, sp, -16
    sw ra, 12(sp)
    sw s2, 8(sp)
    sw s3, 4(sp)
    sw s0, 0(sp)

    bge s2, s3, quicksort_end  # if low >= high: return

    # Partition
    call partition

    # Save returned pivot index in t0
    mv t0, a0

    # Recursively sort left part
    mv s3, t0
    addi s3, s3, -1
    call quicksort

    # Restore state
    lw s0, 0(sp)
    lw s2, 8(sp)
    lw s3, 4(sp)

    # Recursively sort right part
    mv s2, t0
    addi s2, s2, 1
    call quicksort

quicksort_end:
    lw ra, 12(sp)
    lw s2, 8(sp)
    lw s3, 4(sp)
    lw s0, 0(sp)
    addi sp, sp, 16
    ret

# int partition(int* arr, int low, int high)
partition:
    addi sp, sp, -16
    sw ra, 12(sp)
    sw s2, 8(sp)
    sw s3, 4(sp)
    sw s0, 0(sp)

    # pivot = arr[high]
    slli t0, s3, 2         # offset = high * 4
    add t0, s0, t0         # &arr[high]
    lw t1, 0(t0)           # t1 = pivot

    addi t2, s2, -1        # t2 = i = low - 1
    mv t3, s2              # t3 = j = low

partition_loop:
    bgt t3, s3, partition_done

    slli t4, t3, 2         # offset = j * 4
    add t4, s0, t4
    lw t5, 0(t4)           # t5 = arr[j]

    bgt t5, t1, skip_swap

    addi t2, t2, 1         # i++
    slli t6, t2, 2
    add t6, s0, t6
    lw a0, 0(t6)
    sw t5, 0(t6)           # arr[i] = arr[j]
    sw a0, 0(t4)           # arr[j] = arr[i]

skip_swap:
    addi t3, t3, 1
    j partition_loop

partition_done:
    addi t2, t2, 1
    slli t4, t2, 2
    add t4, s0, t4         # arr[i+1]
    slli t6, s3, 2
    add t6, s0, t6         # arr[high]
    lw a0, 0(t6)
    lw t5, 0(t4)
    sw t5, 0(t6)
    sw a0, 0(t4)

    mv a0, t2              # return i+1

    lw ra, 12(sp)
    lw s2, 8(sp)
    lw s3, 4(sp)
    lw s0, 0(sp)
    addi sp, sp, 16
    ret
