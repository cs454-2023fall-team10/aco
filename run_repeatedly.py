import aco

file_path = "./fitness/functions.py"
graph_name = "kakaotalk-faq-231129-small-mingled-001"

lines = None
distance_line = 0
alpha_line = 0
best_fitness = 0
best_graph = None
best_threshold = 0
best_alpha = 0

with open(file_path, 'r') as file:
    lines = file.readlines()

file.close()

# Modify the DISTANCE_THRESHOLD value
for i, line in enumerate(lines):
    if 'DISTANCE_THRESHOLD =' in line:
        distance_line = i
    if 'alpha =' in line :
        alpha_line = i

for new_threshold in range(1, 10) :
    for new_alpha in range(1, 10) :
        parts = lines[distance_line].split('=')
        parts[1] = f' {new_threshold / 10}\n'  # Update the value
        lines[distance_line] = '='.join(parts)

        parts = lines[alpha_line].split('=')
        parts[1] = f' {new_alpha / 10}\n'  # Update the value
        lines[alpha_line] = '='.join(parts)

        # Write the modified content back to the file
        with open(file_path, 'w') as write_file:
            write_file.writelines(lines)

        write_file.close()

        fitness, optimized_CG = aco.run_another(graph_name)
        if fitness > best_fitness :
            best_graph = optimized_CG
            best_threshold = new_threshold / 10
            best_alpha = new_alpha / 10
            best_fitness = fitness

print("Best distance: {}, Best alpha: {}, Best fitness: {}".format(best_threshold, best_alpha, best_fitness))
aco.draw_back(graph_name, best_graph)