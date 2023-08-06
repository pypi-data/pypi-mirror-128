#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>


struct s_buffer {
    size_t      size;
    void        *data;
};


static struct s_buffer *create_buffer(const size_t size)
{
struct s_buffer     *buffer;

    buffer = malloc(sizeof(*buffer) + size);
    if (!buffer)
        return (NULL);
    buffer->data = (void*)((size_t)buffer + sizeof(*buffer));
    return (buffer);
}

int     main(void)
{
    struct s_buffer     *shit;

    shit = create_buffer(200);
    if (!shit)
        return (EXIT_FAILURE);
    free(shit);
    strcpy(shit->data, "This is my shit\n");
    printf("%s", (char*)shit->data);
    bzero(shit->data, 200);
    return (EXIT_SUCCESS);
}
