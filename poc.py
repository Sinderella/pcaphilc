import argparse
import sys
from os import path

import matplotlib.pyplot as plt
from hilbertcurve.hilbertcurve import HilbertCurve
from scapy.all import rdpcap

max_p = 20  # the number of iterations used in constructing the Hilbert curve (must be > 0)
N = 2  # the number of dimensions (must be > 0)
color = 'red'


def main(input_file, output_file):
    plt.figure(figsize=(10, 10))
    packets = rdpcap(input_file)

    packet_times = []
    packet_time_min = None

    for packet in packets:
        # lib doesn't support float
        packet_time = int(packet.time * 1000000)
        packet_times.append(packet_time)

        if packet_time_min is None:
            packet_time_min = packet_time
        elif packet_time < packet_time_min:
            packet_time_min = packet_time

    # convert to relative
    relative_packet_times = [
        packet_time - packet_time_min for packet_time in packet_times
    ]

    for p in range(1, max_p):
        hc = HilbertCurve(p, N)
        pts = []

        try:
            for packet_time in relative_packet_times:
                pts.append(hc.coordinates_from_distance(packet_time))
        except ValueError:
            continue

        print(f'Computing with N={N}, p={p}')

        for i in range(len(pts) - 1):
            plt.scatter(pts[i][0], pts[i][1], 60, color=color)
        break

    plt.xlabel('x')
    plt.ylabel('y')
    plt.tight_layout()
    plt.savefig(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', help='path to pcap file')
    parser.add_argument('-o', '--output', help='path to output image file')

    args = parser.parse_args()

    input_file = path.realpath(args.input)
    output_file = path.realpath(args.output)

    main(args.input, args.output)
