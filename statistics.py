import api_connect
import sys


class ExamEntry:
    def __init__(self, voivodeship, year, amount_of_taken, amount_of_passed):
        self.voivodeship = voivodeship
        self.year = year
        self.amount_of_taken = amount_of_taken
        self.amount_of_passed = amount_of_passed
        self.pass_rate = self.amount_of_passed / self.amount_of_taken


class Statistics:
    def __init__(self):
        api = api_connect.APIConnect()
        self.matura_file = self.populate_exam_list(api.get_matura_file().split('\r\n'))
        if self.matura_file == 0:
            sys.exit('Could not load a file from an API')

    def populate_exam_list(self, exam_file):
        exam_list = []

        class ExamTmp:
            def __init__(self, passed, taken):
                self.passed = passed
                self.taken = taken

        exam_by_voivodeship = {}
        for line in exam_file[1:]:

            line_content = line.split(';')
            if line != '' and line_content[0] != 'Polska':
                if line_content[1] == 'przystąpiło':
                    type = 'take'
                elif line_content[1] == 'zdało':
                    type = 'pass'

                key = line_content[0] + '+' + line_content[3]
                if key in exam_by_voivodeship:
                    if line_content[1] == 'przystąpiło':
                        exam_by_voivodeship[key].taken += int(line_content[4])
                    elif line_content[1] == 'zdało':
                        exam_by_voivodeship[key].passed += int(line_content[4])
                else:
                    if line_content[1] == 'przystąpiło':
                        exam_by_voivodeship[key] = ExamTmp(0, int(line_content[4]))
                    elif line_content[1] == 'zdało':
                        exam_by_voivodeship[key] = ExamTmp(int(line_content[4]), 0)

        for key, value in exam_by_voivodeship.items():
            key_split = key.split('+')
            voivodeship = key_split[0]
            year = int(key_split[1])
            exam_list.append(ExamEntry(voivodeship, year, value.taken, value.passed))

        return exam_list

    def average_per_voivodeship(self, voivodeship, to_year):
        entries = (filter(lambda x: x.voivodeship == voivodeship, self.matura_file))

        average = 0.0
        count = 0
        for entry in entries:
            year = entry.year
            amount_of_ppl = entry.amount_of_taken
            if year > to_year:
                break
            average += amount_of_ppl
            count += 1

        if count != 0:
            average /= count
            print("%d - %.2f" % (to_year, average))

            return average
        else:
            print("There are no data for given year")
            return 0

    def pass_rate_percentage(self, voivodeship):
        entries = (filter(lambda x: x.voivodeship == voivodeship, self.matura_file))

        for entry in entries:
            print("%d - %.2f%%" % (entry.year, entry.pass_rate * 100))

    def best_pass_rate_for_voivodeship(self, year):
        entries = filter(lambda x: x.year == year, self.matura_file)

        max_pass_rate = 0
        best_voivodeship = ''
        for entry in entries:
            if entry.pass_rate > max_pass_rate:
                max_pass_rate = entry.pass_rate
                best_voivodeship = entry.voivodeship
        if best_voivodeship != '':
            print("%d - %s" % (year, best_voivodeship))
        else:
            print("There is no best voivodeship for given year")

    def pass_rate_regression_by_voivodeship(self):
        pass_rates_by_voivodeship = {}

        class ExamTmp:
            def __init__(self, year, pass_rate):
                self.year = year
                self.pass_rate = pass_rate

        for entry in self.matura_file:
            if entry.voivodeship in pass_rates_by_voivodeship:
                pass_rates_by_voivodeship[entry.voivodeship].append(ExamTmp(entry.year, entry.pass_rate))
            else:
                pass_rates_by_voivodeship[entry.voivodeship] = [ExamTmp(entry.year, entry.pass_rate)]

        is_printed = False
        for voiv, entry in pass_rates_by_voivodeship.items():
            entry.sort(key=lambda x: x.year)
            prev_pass_rate = 0.0
            for ent in entry:
                if ent.pass_rate < prev_pass_rate:
                    print("%s : %d (%.2f) -> %d (%.2f)" % (voiv, ent.year - 1, prev_pass_rate, ent.year, ent.pass_rate))
                    is_printed = True
                prev_pass_rate = ent.pass_rate

        if not is_printed:
            print("No regression seen!")

    def voivodeship_comparison(self, voivodeship_1, voivodeship_2):
        voiv1 = list(filter(lambda x: x.voivodeship == voivodeship_1, self.matura_file))
        voiv2 = list(filter(lambda x: x.voivodeship == voivodeship_2, self.matura_file))

        voiv1.sort(key=lambda x: x.year)
        voiv2.sort(key=lambda x: x.year)

        for i in range(0, len(voiv1)):
            if i >= len(voiv2):
                break

            if voiv1[i].pass_rate > voiv2[i].pass_rate and voiv1[i].year == voiv2[i].year:
                print("%d - %s" % (voiv1[i].year, voiv1[i].voivodeship))
            elif voiv1[i].pass_rate < voiv2[i].pass_rate and voiv1[i].year == voiv2[i].year:
                print("%d - %s" % (voiv2[i].year, voiv2[i].voivodeship))
            elif voiv1[i].pass_rate == voiv2[i].pass_rate and voiv1[i].year == voiv2[i].year:
                print("%d - ex aequo %s and %s" % (voiv2[i].year, voiv1[i].voivodeship, voiv2[i].year))