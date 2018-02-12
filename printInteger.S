	xorl 	%esi, %esi

loop:
	mov 	$0, %edx
	mov 	$10, %ebx
	div 	%ebx
	add 	$48, %edx
	push 	%edx
	inc 	%esi
	cmp 	$0, %eax
	jz next
	jmp loop

next:
	cmpl 	$0, %esi
	jz nextnext
	dec 	%esi
	mov     $4, %eax                # system call 4 is write
	mov     $1, %ebx                # file handle 1 is stdout
        mov     %esp, %ecx          # address of string to output
        mov     $1, %edx               # number of bytes to write
        int     $0x80                   # invoke operating system code
	add 	$4, %esp
	jmp next
 
nextnext:        
	mov     $4, %eax                # system call 4 is write
	mov     $1, %ebx                # file handle 1 is stdout
	mov	$message, %ecx          # address of string to output
	mov     $1, %edx               # number of bytes to write
	add 	$4, %esp
	int     $0x80                   # invoke operating system code
    leave 
	ret
