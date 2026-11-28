"""Console menu demonstrating sorting and the graph container."""

from array import array
from typing import Callable, Iterable, Optional

from .drawing import draw_graph
from .graph import Graph, GraphError, Vertex
from .models import Student
from .sorting import bubble_sort, patience_sort

EXIT_CHOICE = "0"
DESCENDING_ANSWER = "д"
EMPTY_LIST_MARK = "  (добавьте вершины, чтобы увидеть граф)"
NO_NEIGHBOURS_MARK = "-"
SAMPLE_INTS = [5, 2, 9, 1, 5, 6, -3]
SAMPLE_WORDS = ["груша", "яблоко", "инжир", "банан"]
SAMPLE_STUDENTS = [Student(8.5, "Ольга"), Student(9.1, "Иван"), Student(7.2, "Пётр"), Student(9.1, "Анна")]

MAIN_MENU = "\n1. Демонстрация сортировки\n2. Демонстрация графа\n0. Выход"
SORT_MENU = "\nДанные: 1. числа  2. слова  3. студенты  4. массив чисел  5. свои числа  0. Назад"
GRAPH_MENU = (
    "\n1. Добавить вершину  2. Добавить ребро  3. Удалить вершину  4. Удалить ребро  5. Показать граф\n"
    "6. Информация о вершине  7. Степень ребра  8. Обратный порядок вершин  9. Копия и сравнение\n"
    "10. Нарисовать граф  0. Назад"
)


class Console:
    """Small wrapper over input/print so the menu can be tested."""

    def __init__(self, read: Callable[[str], str] = input, write: Callable[[str], None] = print) -> None:
        self.read = read
        self.write = write

    def ask(self, prompt: str) -> str:
        return self.read(prompt).strip()

    def ask_int(self, prompt: str) -> int:
        try:
            return int(self.ask(prompt))
        except ValueError:
            raise ValueError("Введите целое число") from None


def build_sort_data(choice: str, console: Console) -> Optional[object]:
    """Return the data set picked in the sorting menu, or None for an unknown choice."""
    builders = {
        "1": lambda: list(SAMPLE_INTS),
        "2": lambda: list(SAMPLE_WORDS),
        "3": lambda: list(SAMPLE_STUDENTS),
        "4": lambda: array("i", SAMPLE_INTS),
        "5": lambda: [int(word) for word in console.ask("Числа через пробел: ").split()],
    }
    builder = builders.get(choice)
    return builder() if builder else None


def handle_safely(console: Console, handle: Callable[[str], None], choice: str) -> None:
    try:
        handle(choice)
    except (GraphError, ValueError) as error:
        console.write(f"Ошибка: {error}")


def menu_loop(console: Console, menu: str, handle: Callable[[str], None]) -> None:
    """Show the menu until the user exits; report recoverable errors instead of crashing."""
    while True:
        console.write(menu)
        choice = console.ask("Выбор: ")
        if choice == EXIT_CHOICE:
            return
        handle_safely(console, handle, choice)


def run_sorting(console: Console) -> None:
    algorithms = {"1": ("Сортировка пузырьком", bubble_sort), "2": ("Пасьянсная сортировка", patience_sort)}

    def handle(choice: str) -> None:
        data = build_sort_data(choice, console)
        if data is None:
            console.write("Неизвестный пункт меню")
        else:
            sort_with_chosen_algorithm(console, data, algorithms)

    menu_loop(console, SORT_MENU, handle)


def format_items(items: Iterable) -> str:
    return ", ".join(str(item) for item in items)


def sort_with_chosen_algorithm(console: Console, data: object, algorithms: dict) -> None:
    name, algorithm = algorithms.get(console.ask("Алгоритм: 1. Пузырёк  2. Пасьянс: "), (None, None))
    if algorithm is None:
        console.write("Неизвестный алгоритм")
        return
    descending = console.ask("По убыванию? (д/н): ").lower() == DESCENDING_ANSWER
    console.write(f"До:      {format_items(data)}")
    algorithm(data, reverse=descending)
    console.write(f"После:   {format_items(data)}  <- {name}")


def pick_vertex(graph: Graph, console: Console, prompt: str = "Номер вершины: ") -> Vertex:
    number = console.ask_int(prompt)
    vertices = list(graph.vertex_iterator())
    if not 1 <= number <= len(vertices):
        raise GraphError(f"Нет вершины с номером {number}")
    return vertices[number - 1]


def add_vertex(graph: Graph, console: Console) -> None:
    graph.add_vertex(console.ask("Значение вершины: "))


def add_edge(graph: Graph, console: Console) -> None:
    graph.add_edge(
        pick_vertex(graph, console, "Номер первой вершины: "), pick_vertex(graph, console, "Номер второй вершины: ")
    )


def remove_vertex(graph: Graph, console: Console) -> None:
    graph.remove_vertex(pick_vertex(graph, console))


def remove_edge(graph: Graph, console: Console) -> None:
    graph.remove_edge(
        pick_vertex(graph, console, "Номер первой вершины: "), pick_vertex(graph, console, "Номер второй вершины: ")
    )


def matrix_lines(graph: Graph, vertices: list) -> list:
    width = len(str(len(vertices)))

    def cell(text: object) -> str:
        return str(text).rjust(width)

    header = "  ".join(cell(number) for number in range(1, len(vertices) + 1))
    rows = [
        f"  {cell(number)}  " + "  ".join(cell(int(graph.has_edge(row, column))) for column in vertices)
        for number, row in enumerate(vertices, 1)
    ]
    return [f"  {cell('')}  {header}", *rows]


def adjacency_lines(graph: Graph, vertices: list) -> list:
    numbers = {id(vertex): number for number, vertex in enumerate(vertices, 1)}
    lines = []
    for vertex in vertices:
        neighbours = ", ".join(f"{numbers[id(item)]} ({item.value})" for item in graph.adjacent_vertex_iterator(vertex))
        lines.append(f"  {numbers[id(vertex)]} ({vertex.value}): {neighbours or NO_NEIGHBOURS_MARK}")
    return lines


def describe_graph(graph: Graph) -> str:
    vertices = list(graph.vertex_iterator())
    if not vertices:
        return f"Граф пуст\n{EMPTY_LIST_MARK}"
    sections = [
        f"Вершин: {graph.vertex_count()}, рёбер: {graph.edge_count()}",
        "Матрица смежности:",
        *matrix_lines(graph, vertices),
        "Список смежности:",
        *adjacency_lines(graph, vertices),
    ]
    return "\n".join(sections)


def show_graph(graph: Graph, console: Console) -> None:
    console.write(describe_graph(graph))


def draw(graph: Graph, console: Console) -> None:
    if graph.empty():
        console.write(EMPTY_LIST_MARK)
        return
    console.write(draw_graph(graph))
    legend = ", ".join(f"({number})={vertex.value}" for number, vertex in enumerate(graph.vertex_iterator(), 1))
    console.write(f"Вершины: {legend}")


def vertex_info(graph: Graph, console: Console) -> None:
    vertex = pick_vertex(graph, console)
    console.write(f"Степень: {graph.degree(vertex)}")
    console.write(f"Смежные вершины: {[item.value for item in graph.adjacent_vertex_iterator(vertex)]}")
    console.write(
        f"Инцидентные рёбра: {[(e.first.value, e.second.value) for e in graph.incident_edge_iterator(vertex)]}"
    )


def edge_degree(graph: Graph, console: Console) -> None:
    first = pick_vertex(graph, console, "Номер первой вершины: ")
    second = pick_vertex(graph, console, "Номер второй вершины: ")
    console.write(f"Степень ребра: {graph.edge_degree(first, second)}")


def reverse_order(graph: Graph, console: Console) -> None:
    console.write(f"Вершины в обратном порядке: {[vertex.value for vertex in graph.reverse_vertex_iterator()]}")


def copy_and_compare(graph: Graph, console: Console) -> None:
    clone = graph.copy()
    console.write(f"Копия:\n{describe_graph(clone)}")
    console.write(f"копия == оригинал: {clone == graph}")
    clone.add_vertex("лишняя")
    console.write(f"После добавления вершины в копию: равны={clone == graph}, копия > оригинал={clone > graph}")


GRAPH_ACTIONS = {
    "1": add_vertex,
    "2": add_edge,
    "3": remove_vertex,
    "4": remove_edge,
    "5": show_graph,
    "6": vertex_info,
    "7": edge_degree,
    "8": reverse_order,
    "9": copy_and_compare,
    "10": draw,
}


def run_graph(console: Console) -> None:
    graph: Graph = Graph()

    def handle(choice: str) -> None:
        action = GRAPH_ACTIONS.get(choice)
        if action is None:
            console.write("Неизвестный пункт меню")
        else:
            action(graph, console)

    menu_loop(console, GRAPH_MENU, handle)


def run(console: Optional[Console] = None) -> None:
    console = console or Console()
    sections = {"1": run_sorting, "2": run_graph}
    while True:
        console.write(MAIN_MENU)
        choice = console.ask("Выбор: ")
        if choice == EXIT_CHOICE:
            return
        section = sections.get(choice)
        section(console) if section else console.write("Неизвестный пункт меню")
