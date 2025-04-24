    .data
base:           .word   0   # граф начнется отсюда (25 значений, 5x5)
                .word   0, 10, 0,  30, 100
                .word   10, 0,  50, 0,  0
                .word   0,  50, 0,  20, 10
                .word   30, 0,  20, 0,  60
                .word   100, 0, 10, 60, 0

dist:           .word   0, 9999, 9999, 9999, 9999
visited:        .word   0, 0, 0, 0, 0

    .text
    .globl _start
_start:
    li s0, 5              # s0 = n (кол-во вершин)
    la s1, base           # s1 = addr(matrix)
    la s2, dist           # s2 = addr(dist)
    la s3, visited        # s3 = addr(visited)

outer_loop:
    li t0, -1             # t0 = min_index = -1
    li t1, 9999           # t1 = min_dist = MAX

    li t2, 0              # t2 = i
find_min_loop:
    bge t2, s0, found_min

    slli t3, t2, 2        # offset = i*4
    add t4, s2, t3        # &dist[i]
    lw t5, 0(t4)          # dist[i]

    add t6, s3, t3        # &visited[i]
    lw s4, 0(t6)          # visited[i]
    bne s4, zero, skip_i  # if visited[i] != 0 → skip

    bge t5, t1, skip_i    # if dist[i] >= min_dist → skip

    mv t1, t5             # min_dist = dist[i]
    mv t0, t2             # min_index = i

skip_i:
    addi t2, t2, 1
    j find_min_loop

found_min:
    blt t0, zero, end     # если min_index == -1, конец

    slli t3, t0, 2
    add t4, s3, t3
    li t5, 1
    sw t5, 0(t4)          # visited[min_index] = 1

    li t2, 0              # j = 0
update_loop:
    bge t2, s0, outer_continue

    slli t6, t2, 2
    add s4, s3, t6
    lw s5, 0(s4)
    bne s5, zero, skip_j  # if visited[j] != 0 → continue

    mul s6, t0, s0        # row = min_index * n
    add s6, s6, t2        # row + j
    slli s6, s6, 2
    add s7, s1, s6       # &matrix[min_index][j]
    lw s8, 0(s7)        # weight

    beq s8, zero, skip_j # if weight == 0 → skip

    slli s9, t0, 2
    add s10, s2, s9
    lw s11, 0(s10)        # dist[min_index]

    add a1, s11, s8     # alt = dist[min_index] + weight

    add a2, s2, t6
    lw a3, 0(a2)        # dist[j]
    bge a3, a1, update_dist
    j skip_j

update_dist:
    sw a1, 0(a2)        # dist[j] = alt

skip_j:
    addi t2, t2, 1
    j update_loop

outer_continue:
    j outer_loop

end:
    # halt или бесконечный цикл
    wfi
