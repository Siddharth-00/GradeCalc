import json

class Component:
    
    def __init__(self, name) -> None:
        self.name = name
        self.subcomponents = {}
        self.mark = None
        self.percentage_taken = 0
        self.provisional_mark = 0
        
    def add_subcomponent(self, comp, weight):
        self.subcomponents[comp.name] = (comp, weight)
        
    def set_mark(self, mark):
        self.mark = self.provisional_mark = mark

    def generate_stats(self):
        if self.mark is not None:
            self.percentage_taken = 1
        else:
            for comp,w in self.subcomponents.values():
                comp.generate_stats()
                self.percentage_taken += comp.percentage_taken * w
                self.provisional_mark += comp.provisional_mark * w * comp.percentage_taken
            if self.percentage_taken > 0:    
                self.provisional_mark /= self.percentage_taken

def print_stats(root: Component):
    print("\033[1mWHOLE YEAR\033[0m")
    print(f"{'Percentage Completed':<30} {'Provisional Mark':<30}")
    print(f"{'-' * 10:<30} {'-' * 10:<30}")
    print(f"{str(round(root.percentage_taken * 100, 2)) + '%':<30} {str(round(root.provisional_mark * 100, 2)) + '%':<30}")
    print()
    print()
    print("\033[1mMODULES\033[0m")
    print(f"{'Module Name':<40} {'Percentage Completed':<40} {'Provisional Mark':<40}")
    print(f"{'-' * 10:<40} {'-' * 10:<40} {'-' * 10:<40}")
    for module,_ in root.subcomponents.values():
        name = f"{module.name}"
        print(f"{name:<40} {str(round(module.percentage_taken * 100, 2)) + '%':<40} {str(round(module.provisional_mark * 100, 2)) + '%':<40}")
    print()
    
def calculate_grade():
    with open("grades.json") as f:
        data = json.load(f)

    root = Component("Year")
    modules = data["modules"]
    total_credits = sum(modules[m]["credits"] for m in modules)
    for m in modules:
        module = Component(m)
        root.add_subcomponent(module, modules[m]["credits"] / total_credits)
        components = modules[m]["components"]
        for comp in components:
             new_comp = Component(comp)
             module.add_subcomponent(new_comp, components[comp]["weighting"])
             if "mark" in components[comp]:
                 new_comp.set_mark(components[comp]["mark"])
    root.generate_stats()
    print_stats(root)
        
    
if __name__ == "__main__":
   calculate_grade()