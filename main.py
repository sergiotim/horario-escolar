from ortools.sat.python import cp_model

model = cp_model.CpModel()


teachers = ["Ana Andrade", "Bianca Bolada", "Carlos Cabeção"]

classes = ["6A","7B","8A"]

slots = ["Seg8","Seg9","Seg10"]

# Lista de tuplas: (Professor, Turma, Quantidade de Aulas)
requirements = [
    (teachers[0], classes[0], 1), # Ana dá 1 aula na 6A
    (teachers[0], classes[1], 1), # Ana dá 1 aula na 7B
    (teachers[0], classes[2], 1), # Ana dá 1 aula na 8A
    (teachers[1], classes[1], 2), # Bianca dá 1 aula na 7B
    (teachers[1], classes[0], 1), # Bianca dá 1 aula na 6A
    (teachers[2], classes[2], 1), # Carlos dá 1 aula na 8A
    (teachers[2], classes[0], 1), # Carlos dá 1 aula na 6A
    # Pode adicionar mais se quiser testar conflitos depois
]

combinations = {}

for teacher in teachers:
    for i_class in classes:
        for slot in slots:
            var = model.NewBoolVar(f"t_{teacher}_c_{i_class}_s_{slot}")
            combinations[(teacher,i_class,slot)] = var

# print(combinations[("Bianca Bolada","6A","Seg9")])
for teacher in teachers:
    for slot in slots:
        var_for_sum = []

        for i_class in classes:
            var = combinations[(teacher,i_class,slot)]

            var_for_sum.append(var)

        model.Add(sum(var_for_sum) <= 1)



for i_class in classes:
    for slot in slots:
        var_for_sum = []

        for teacher in teachers:
            var = combinations[(teacher,i_class,slot)]

            var_for_sum.append(var)

        model.Add(sum(var_for_sum) <= 1)
            
            
for requirement in requirements:
    var_for_sum = []    
    for slot in slots:
        var = combinations[(requirement[0],requirement[1],slot)]

        var_for_sum.append(var)

    model.Add(sum(var_for_sum) == requirement[2])


solver = cp_model.CpSolver()

status = solver.Solve(model)



if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    header = f"{'TURMA':<10} |"

    for slot in slots:
        header += f" {slot:<15} |"
    
    print(header)
    print("-" * len(header))

    for i_class in classes:
        row_text = f"{i_class:<10} |"

        for slot in slots:
            teacher_found = " - "

            for teacher in teachers:
                
                var = combinations[(teacher,i_class,slot)]

                if solver.Value(var) == 1:
                    teacher_found = teacher
                    break

            row_text += f" {teacher_found:<15} |"
        
        print(row_text)
else:
    print("Não foi possível encontrar uma solução")

