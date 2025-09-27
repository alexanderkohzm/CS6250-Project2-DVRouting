from Topology import *
from Node import *
from helpers import *

import pytest

topo_list = [
    # From the assignment
    'ComplexTopo',
    'SimpleNegativeCycleTopo',
    'SimpleTopo',
    'SingleLoopTopo',

    # Others
    'LargeRandom',
    'n_longAlternatingSeries',
    'n_longNegSeries',
    'n_longNegSeries2',
    'n_longSeries',
    'new_ComplexTopoHalfed',
    'new_LongLoop',
    'new_NegCycleWithBiNegLink',
    'new_NoNegTopo',
    'new_TailNegativeCycle',
    'new_TailNegCycleWithBiNegLink',
    'new_v2_SingleNode',
    'new_v2_TwoNodes',
    'new_v2_TwoNodesNeg',
    'new_v2_TwoNodesUni',
    'new_v2_VeryComplex',
    'new_v2_VeryComplex2',
    'new_YoutubeTopo',
    'NodeDetectEarly',
    'NodeDetectWithCycle',
    'NoInOrOutLinks',
    'SimpleNegativeCycle',
    'SimpleOddLengthNegativeCycle',
    'SimpleTopo',
    'SingleLoopTopo',
    'TwoNegCycles'
]

@pytest.mark.parametrize("f_name", topo_list)
class TestTopos:
    def test_distance_vectors(self, f_name):
        try:
            with open(f'./logs/{f_name}.log') as f:
                 expected_logs = [l.strip() for l in f.readlines()]
        except FileNotFoundError:
                pytest.skip(f"Missing log file for {f_name}, skipping test.")

        with open(f'./logs/{f_name}.log') as f:
            expected_logs = [l.strip() for l in f.readlines()]
        last_output_expected = []
        for x in reversed(expected_logs[:-1]):
            if x == "-----":
                break
            last_output_expected.append(x)
        expected = {}
        for line in last_output_expected:
            node, dv = line.split(":")
            expected[node] = {}
            for s in dv.split(" "):
                n, w = s[1:-1].split(",")
                expected[node].setdefault(n, w)


        open_log(f_name + ".log")
        topo = Topology(f_name + ".txt")
        topo.run_topo()
        finish_log()

        with open(f_name + ".log") as f:
            actual_logs = [l.strip() for l in f.readlines()]
        last_output_actual = []
        for x in reversed(actual_logs[:-1]):
            if x == "-----":
                break
            last_output_actual.append(x)
        actual = {}
        for line in last_output_actual:
            node, dv = line.split(":")
            actual[node] = {}
            for s in dv.split(" "):
                n, w = s[1:-1].split(",")
                actual[node].setdefault(n, w)

        assert actual == expected
