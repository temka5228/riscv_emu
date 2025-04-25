    .data
N:          .word 32
adj:        .space 4096     # матрица смежности (adj[i][j] = 1 или 0)
visited:    .space 128
stack:      .space 512        # стек (размер 64)

    .text
    .globl _start
_start:
    la      s0, adj
    la      s1, visited
    la      s2, stack
    li      s3, 0    
    li a5, 16          # top = 0

    # Заполняем visited нулями
    li      t0, 0
zero_visited:
    sw      x0, 0(s1)
    addi    s1, s1, 4
    addi    t0, t0, 1
    li      t1, 16
    blt     t0, t1, zero_visited
    la      s1, visited        # восстановим s1

    # stack[0] = 0 (начинаем с вершины 0)
    sw      x0, 0(s2)          # stack[0] = 0

dfs_loop:
    # if top < 0: конец
    blt     s3, x0, done

    # node = stack[top]
    slli    t0, s3, 2
    add     t1, s2, t0
    lw      t2, 0(t1)          # t2 = node

    # top--
    addi    s3, s3, -1

    # if visited[node] == 1 → continue
    slli    t3, t2, 2
    add     t4, s1, t3
    lw      t5, 0(t4)
    bne     t5, x0, dfs_loop   # пропускаем уже посещённую

    # visited[node] = 1
    li      t5, 1
    sw      t5, 0(t4)

    # Цикл по соседям i = 15 → 0 (чтобы DFS шел глубже)
    li      t6, 15
neighbor_loop:
    blt     t6, x0, dfs_loop

    # if adj[node][i] == 1 && !visited[i]
    addi    a7, a5, 0
    li      s7, 0
    jal     mull
    #mul     s7, t2, a5         # row offset = node * 16
    add     s7, s7, t6         # index = node*16 + i
    slli    s7, s7, 2
    add     s8, s0, s7
    lw      s9, 0(s8)          # s9 = adj[node][i]

    beq     s9, x0, skip_neighbor

    slli    s10, t6, 2
    add     s11, s1, s10
    lw      s6, 0(s11)
    bne     s6, x0, skip_neighbor

    # push i на стек
    addi    s3, s3, 1
    slli    s5, s3, 2
    add     s5, s2, s5
    sw      t6, 0(s5)

skip_neighbor:
    addi    t6, t6, -1
    j       neighbor_loop
    
mull: 
	add s7, s7, t2
	addi a7, a7, -1
	bge a7, zero, mull
	ret

done:
    ecall
