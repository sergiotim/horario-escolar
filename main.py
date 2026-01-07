from ortools.sat.python import cp_model
import json

model = cp_model.CpModel()


with open('scenario.json',"r",encoding="utf-8") as file:
    data = json.load(file)

teachers_map = {t["id"]: t["name"] for t  in data["teachers"]}
teachers_id = list(teachers_map.keys())

classes_map = {c['id']: c['name'] for c in data['classes']}
classes_id = list(classes_map.keys())

slots = data["slots"]

# --- ADAPTAÇÃO DOS REQUIREMENTS ---
# Como o JSON usa NOMES, mas o solver agora quer IDs, precisamos converter.
# Criamos um mapa reverso temporário: {'Ana Andrade': 'p1'}
name_to_id_teacher = {v: k for k, v in teachers_map.items()}
name_to_id_class = {v: k for k, v in classes_map.items()}

requirements = []
for req in data["requirements"]:
    # traduz o nome para ID antes de guardar
    t_id = name_to_id_teacher[req['teacher_name']]
    c_id = name_to_id_class[req['class_name']]
    count = req['count']
    requirements.append((t_id, c_id, count))

combinations = {}

for teacher in teachers_id:
    for i_class in classes_id:
        for slot in slots:
            var_name = f"t_{teacher}_c_{i_class}_s_{slot}"
            var = model.NewBoolVar(var_name)
            
            combinations[(teacher, i_class, slot)] = var


for teacher in teachers_id:
    for slot in slots:
        var_for_sum = []

        for i_class in classes_id:
            var = combinations[(teacher,i_class,slot)]

            var_for_sum.append(var)

        model.Add(sum(var_for_sum) <= 1)



for i_class in classes_id:
    for slot in slots:
        var_for_sum = []

        for teacher in teachers_id:
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
    print("\n" + "="*60)
    print(f"{'HORÁRIO':<15} |", end="") # Cabeçalho da primeira coluna
    
    # Cabeçalho das colunas (Nomes das Turmas)
    for i_class in classes_id:
        c_name = classes_map[i_class]
        print(f" {c_name:<15} |", end="")
    print("\n" + "-"*85)

    # CORPO DA TABELA
    # Agora a linha é o SLOT (Horário)
    for slot in slots:
        row_text = f"{slot:<15} |"
        
        # E as colunas são as TURMAS
        for i_class in classes_id:
            teacher_found = " - "
            
            # Buscamos quem dá aula nessa turma, nesse horário
            for teacher in teachers_id:
                if solver.Value(combinations[(teacher, i_class, slot)]) == 1:
                    teacher_found = teachers_map[teacher]
                    break
            
            # Truque para encurtar nomes muito longos (pega só os primeiros 15 chars)
            row_text += f" {teacher_found[:15]:<15} |"
        
        print(row_text)
        
        # Adiciona uma linha separadora entre os dias para facilitar a leitura
        if "10" in slot: # Se for o último horário do dia
            print("-" * 85)

else:
    print("Não foi possível encontrar uma solução.")

