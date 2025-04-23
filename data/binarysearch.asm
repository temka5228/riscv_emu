# binary_search.s

.data
    array: .word 1, 3, 5, 7, 9, 11, 13, 15, 17, 19  # Отсортированный массив
    key:   .word 11                                # Ключ для поиска
    size:  .word 10                                # Размер массива

.text
.globl _start

_start:
    # Загрузка адреса массива (array) в t0
    la t0, array

    # Загрузка размера массива (size) в t1
    lw t1, size

    # Загрузка ключа (key) в t2
    lw t2, key

    # Инициализация low и high
    li t3, 0       # low = 0
    addi t4, t0, -4 # high = -4 (array + size * 4)

loop:
    # Проверка условия выхода из цикла (low > high)
    bgtu t3, t4, not_found

    # Вычисление среднего индекса (mid = (low + high) / 2)
    add t5, t3, t4       # t5 = low + high
    srli t5, t5, 1      # t5 = (low + high) / 2

    # Вычисление адреса элемента по среднему индексу (mid * 4)
    slli t6, t5, 2       # t6 = mid * 4

    add s1, t0, t6
    # Получение значения элемента массива по адресу (array + mid * 4)
    lw t3, 0(s1)        # array[mid]

    # Сравнение найденного элемента с ключом
    beq t3, t2, found   # Если array[mid] == key, поиск успешен
    blt t3, t2, left    # Если array[mid] < key, переходим к поиску в правой половине
    j right             # Если array[mid] > key, переходим к поиску в левой половине

left:
    # Обновление low (low = mid + 1)
    addi t3, t5, 1      # low = mid + 1
    j loop               # Переход к следующей итерации цикла

right:
    # Обновление high (high = mid - 1)
    addi t4, t5, -1     # high = mid - 1
    j loop               # Переход к следующей итерации цикла

found:
    # Поиск успешен. Возвращаем индекс найденного элемента (mid).
    li a7, 93          # syscall exit
    mv a0, t5          # Возвращаем mid в a0
    ecall              # Выход из программы с кодом возврата

not_found:
    # Поиск не удался. Возвращаем -1.
    li a7, 93          # syscall exit
    li a0, -1         # Возвращаем -1 в a0
    ecall              # Выход из программы с кодом возврата
