import statistics
import sys


def main():
    stats = statistics.Statistics()

    if len(sys.argv) <= 1:
        print("You need to pass arguments. Type main.py --help for help")

    if sys.argv[1] == '--help':
        print("""This is a program that counts some statistics for matura exams in Poland.
        
When you type a voivodeship name you need to type it beginning with a capital letter and polish characters
        
    -a, --avg voiv year
        Average amount of people that took an exam in a given voivodeship (voiv) and given year
    
    -pc, --pct voiv
        Percentage pass rate for a given voivodeship (voiv)
        
    -p, --pass-rate year
        A voivodeship with the best pass rate for a given year
    
    -r, --regression
        Voivodeship with regression in pass rate
        
    -c, -comp voiv_1 voiv_2
        A comparison between two voivodeships (voiv_1 and voiv_2)
""")

    elif sys.argv[1] == '--avg' or sys.argv[1] == '-a':
        if len(sys.argv) >= 4:
            try:
                stats.average_per_voivodeship(sys.argv[2], int(sys.argv[3]))
            except ValueError:
                print("Please pass a valid year")
        else:
            print("Too few arguments passed")

    elif sys.argv[1] == '--pct' or sys.argv[1] == '-pc':
        if len(sys.argv) >= 3:
            stats.pass_rate_percentage(sys.argv[2])
        else:
            print("Too few arguments passed")

    elif sys.argv[1] == '--pass-rate' or sys.argv[1] == '-p':
        if len(sys.argv) >= 3:
            try:
                stats.best_pass_rate_for_voivodeship(int(sys.argv[2]))
            except ValueError:
                print("Please pass a valid year")
        else:
            print("Too few arguments passed")

    elif sys.argv[1] == '--regression' or sys.argv[1] == '-r':
        stats.pass_rate_regression_by_voivodeship()

    elif sys.argv[1] == '--comp' or sys.argv[1] == '-c':
        if len(sys.argv) >= 4:
            stats.voivodeship_comparison(sys.argv[2], sys.argv[3])
        else:
            print("Too few arguments passed")


if __name__ == "__main__":
    main()
