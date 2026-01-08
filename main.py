from ortools.sat.python import cp_model


def generate_schedule(teachers, classrooms, slots, requirements):
    """
    Docstring for generate_schedule
    
    :param teachers: dict list with {id,name}
    :param classrooms: dict list with {id,name}
    :param slots: class schedules
    :param requirements: dict list of the number of classes each teacher teaches to a group of students.

    Receives lists of data and returns the resolved time.
    """

    model = cp_model.CpModel()

    teachers_map = {t["id"]: t["name"] for t in teachers}
    teachers_id = list(teachers_map.keys())

    classrooms_map = {c["id"] : c["name"] for c in classrooms}
    classrooms_id = list(classrooms_map.keys())

    schedule_variables = {}

    for teacher in teachers_id:
        for classroom in classrooms_id:
            for slot in slots:
                var_name = f"t_{teacher}_c_{classroom}_s_{slot}"
                var = model.NewBoolVar(var_name)

                schedule_variables[(teacher,classroom,slot)] = var

    for teacher in teachers_id:
        for slot in slots:
            var_for_sum = []

            for classroom in classrooms_id:
                var = schedule_variables[(teacher,classroom,slot)]

                var_for_sum.append(var)

            model.Add(sum(var_for_sum) <=1)

    
    for classroom in classrooms_id:
        for slot in slots:
            var_for_sum = []

            for teacher in teachers_id:
                var = schedule_variables[(teacher,classroom,slot)]

                var_for_sum.append(var)
            
            model.Add(sum(var_for_sum) <= 1)

    for requirement in requirements:
        var_for_sum = []

        for slot in slots:
            var = schedule_variables[(requirement[0],requirement[1],slot)]

            var_for_sum.append(var)

        model.Add(sum(var_for_sum) == requirement[2])

    

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        
        final_schedule = []

        for slot in slots:
            for classroom in classrooms_id:
                for teacher in teachers_id:
                    if solver.Value(schedule_variables[(teacher,classroom,slot)]) == 1:
                        final_schedule.append({
                            "time" : slot,
                            "classroom" : classrooms_map[classroom],
                            "teacher" : teachers_map[teacher]
                        })

        return final_schedule
    else:
        return None

