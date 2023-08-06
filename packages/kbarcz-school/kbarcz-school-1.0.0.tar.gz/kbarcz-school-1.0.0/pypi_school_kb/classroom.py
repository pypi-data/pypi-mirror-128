from pypi_school_kb.student import Student

class Classroom:

    def __init__(self, year_of_creation, classroom_char, students):
        self.students = students
        self.classroom_char = classroom_char
        self.year_of_creation = year_of_creation

    def show_students(self):
        # w pętli wyświetla wszystkich studentów
        print(f'Lista studentów:')
        for student in self.students:
            print(f'L.p. {self.students.index(student)+1} - {student.fullname}')

    def add_student(self, student):
        self.students.append(student)
