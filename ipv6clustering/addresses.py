"""Tools for manipulating and comparing IPv6 addresses.  These functions and
classes are primarly for comparing \64 networks (to preprocess addresses
for clustering to see what live allocations have been."""

import struct
import ipaddress

class SlashIPv6Address(ipaddress.IPv6Address):

    def prefix_int(self, size=64):
        """Returns an integer representation of the prefix of an address.
        So, given `size` as 64 will return the integer value of the \64 prefix
        of the address. The maximum possible value for a prefix to parse is
        64 (given the limitations of the `struct` module).

        Throws:
            ValueError -- If the requested slash prefix size is not between
                          1 and 64 (inclusive)

        Args:
            size -- the slash size of the prefix to return.

        Return:
            The integer value of the slash-prefix of the address
        """
        try:
            return self._prefix_int
        except AttributeError:
            if size < 1 or size > 64:
                msg = "Invalid prefix, must be (0, 64], given {0}".format(size)
                raise ValueError(msg)

            prefix_bytes = self.packed[0:(size / 8)]
            self._prefix_int = struct.unpack(">Q", prefix_bytes)[0]
            return self._prefix_int
