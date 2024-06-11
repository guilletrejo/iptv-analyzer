import datetime
import argparse
from ts.ts_reader import TSReader
from views.viever import Viewer
from ts.ts_stat import Statistics


def main():
    psize = 188
    chunksize = 7
    viewer = Viewer()
    stats = Statistics()
    ts_reader = TSReader()

    stats.onStatReady += viewer.print_stat_result
    stats.onFinalStatReady += viewer.print_final_stat_result

    ts_reader.onPacketDecoded += stats.update_stat
    ts_reader.onPatReceived += stats.update_programs_info
    ts_reader.onPmtReceived += stats.update_programs_info
    ts_reader.onCatReceived += stats.update_programs_info
    ts_reader.onProgramSdtReceived += stats.update_programs_info
    #ts_reader.onSdtReceived += stats.show_table_data
    #ts_reader.onBatReceived += stats.show_table_data
    #ts_reader.onNitReceived += stats.show_table_data

    with open(TS_FILE, 'rb') as file:
        while True:
            data = file.read(psize * chunksize)
            if not data:
                break
            dt = datetime.datetime.now()
            ts_reader.read(data, dt=dt)


    stat = stats.get_stat()
    if stats.pat_received_dt is not None:
        viewer.print_pat(stats.programs.pat, stats.pat_received_dt)
    if stats.pmt_received_dt is not None:
        for pid in stats.programs.get_pmt_pids():
            viewer.print_pmt(stats.programs.get_prog_pmt(pid), stats.pmt_received_dt)
    if stats.sdt_received_dt is not None:
        viewer.print_sdt(stats.programs.sdt, stats.sdt_received_dt)
    if stats.cat_received_dt is not None:
        viewer.print_cat(stats.programs.cat, stats.cat_received_dt)
    viewer.print_stat(stat, stats.programs, ts_reader.known_pids)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze a TS file and monitor its parameters '
                                                 + 'according to ETSI TR 101 290')
    parser.add_argument('-i', "--input", nargs='?', required=True, help='TS file')
    args = vars(parser.parse_args())
    TS_FILE = args['input']
    main()
