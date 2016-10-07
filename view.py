import pstats
p = pstats.Stats('log')
p.strip_dirs().sort_stats('cumulative').print_stats(100)
