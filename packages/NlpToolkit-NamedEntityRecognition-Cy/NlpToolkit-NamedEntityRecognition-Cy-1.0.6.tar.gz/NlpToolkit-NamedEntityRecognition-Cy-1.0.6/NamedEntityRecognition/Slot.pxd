cdef class Slot:

    cdef object type
    cdef str tag

    cpdef object getType(self)
    cpdef str getTag(self)
