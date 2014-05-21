"""Attempt to determine which chunks of the IPv6 address space have beeen
allocated and are in use by finding clusters in a large number of live IPv6
addresses.  This approach uses the DBScan approach, but since we're dealing
with one dimenson of distance, this can be done O(n) time."""

from ipv6clustering.addresses import SlashIPv6Address
import sys
import argparse

parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
parser.add_argument('--input', default=None,
                    help="The path the a list of IPv6 addresses to read and " +
                    "attempt to cluster.  If this is not provided, defaults " +
                    "to stdin.")
parser.add_argument('--output', default=None,
                    help="The path to write the result of the clustering " +
                    "attempt to.  If this is not provided, defaults to stdout.")
parser.add_argument('--dist', default=24, type=int,
                    help="The maximum distance (as a power of two) that " +
                    "can be between two addresses and have them still be " +
                    "considered as being from the same network.")
args = parser.parse_args()

in_handle = open(args.input, 'r') if args.input else sys.stdin
out_handle = open(args.output, 'w') if args.output else sys.stdout

addresses = []
for line in (l.strip().decode() for l in in_handle):
    addresses.append(SlashIPv6Address(line))
addresses.sort(key=lambda x: x.prefix_int())

clusters = [[]]
last_a = None
cluster_dist = 2**args.dist
for a in addresses:
    if not last_a or a.prefix_int() - last_a.prefix_int() < cluster_dist:
        clusters[-1].append(a)
    else:
        clusters.append([a])
    last_a = a

# Now that we have all the clusters extracted, we can print out a rough
# report summarizing our findings
out_handle.write("Processed {0} IPv6 Addresses\n".format(len(addresses)))
out_handle.write("Distance measure of 2^{0} ({1})\n".format(args.dist, cluster_dist))
out_handle.write("Found {0} clusters\n".format(len(clusters)))
out_handle.write("\n")
out_handle.write("----\n")

for c in clusters:
    min_value = c[0].exploded
    max_value = c[-1].exploded
    num_values = len(c)
    out_handle.write("{0} {1} {2}\n".format(min_value, max_value, num_values))
