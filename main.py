import sys
import ctypes
from src.pylogic.functions import logic
from src.pylogic.helpers import floor_to
import src.pylogic.setup as sp

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QScrollArea, QLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QFrame

class MainWindow(QMainWindow):
    spinner_items = []
    spinner_layout = QHBoxLayout()
    item_width = 250

    def __init__(self):
        super().__init__()

        self.setWindowTitle("BOND Calculator")
        
        layout = QVBoxLayout()
        self._build_components(layout) 
        layout.addStretch()

        self._build_spinner(layout)
        
        
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.resize(sp.width, sp.height)

    def _build_components(self, layout: QLayout):
        title = QLabel("Your BOND calculator")
        title.setStyleSheet("font-size: 24px; color: white; font-weight: bold")
        title.setMargin(10)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)

        container = QHBoxLayout()

        leftVBox = QVBoxLayout()

        self.initial_input = QLineEdit()
        self.initial_input.setPlaceholderText("Enter initial amount (26000)")
        self.initial_input.setStyleSheet(sp.input_styles)
        leftVBox.addWidget(self.initial_input)

        self.interest_rate_input = QLineEdit()
        self.interest_rate_input.setPlaceholderText("Enter interest rate (6.25%)")
        self.interest_rate_input.setStyleSheet(sp.input_styles)
        leftVBox.addWidget(self.interest_rate_input)

        self.years_input = QLineEdit()
        self.years_input.setPlaceholderText("Enter BOND's years (10)")
        self.years_input.setStyleSheet(sp.input_styles)
        leftVBox.addWidget(self.years_input)

        controls = QHBoxLayout()

        button_add = QPushButton("Add")
        button_add.setStyleSheet(sp.input_styles)
        button_add.clicked.connect(lambda: self._add(self.initial_input.text(), self.interest_rate_input.text(), self.years_input.text()))
        controls.addWidget(button_add)

        button_calc = QPushButton("Calculate")
        button_calc.setStyleSheet(f"{sp.input_styles}; background-color: green")
        button_calc.clicked.connect(lambda: self._calc(self.initial_input.text(), self.interest_rate_input.text(), self.years_input.text()))
        controls.addWidget(button_calc)

        # Right side
        rightVBox = QVBoxLayout()

        choose_bond = self._build_combo_box()

        rightVBox.addWidget(choose_bond)
        rightVBox.addStretch()

        container.addLayout(leftVBox)
        container.addLayout(rightVBox)
        
        layout.addLayout(container)
        layout.addLayout(controls)

    def _build_combo_box(self):
        combo = QComboBox()
        combo.setStyleSheet("font-size: 18px; padding: 0 4px; margin: 5px")
        
        bonds = getBonds()
        for item in bonds:
            combo.addItem(str(item.name)[2:-1])

        combo.currentTextChanged.connect(self._update_combo)

        return combo
    
    def _update_combo(self, name):
            bonds = getBonds()
            names = [b.name.decode('utf-8') for b in bonds]

            try:
                idx = names.index(name)
                self.interest_rate_input.setText(str(bonds[idx].interest_rate))
                self.years_input.setText(str(bonds[idx].years))
                
            except ValueError:
                print("No bond named COI")

    def _build_spinner(self, layout: QLayout):
        self.row_widget = QWidget()   

        self.row_widget.setFixedWidth(len(self.spinner_items) * self.item_width + len(self.spinner_items)  * sp.margin)              
        self.spinner_layout = QHBoxLayout(self.row_widget)
        self.spinner_layout.setSpacing(sp.margin)  

        self._update_spinner()  

        scroll = QScrollArea()
        scroll.setWidgetResizable(True) 
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame) 
        scroll.setWidget(self.row_widget) 
        scroll.setFixedHeight(120)
        
        layout.addWidget(scroll)
        layout.addStretch()

    def _update_spinner(self):
        clear_layout(self.spinner_layout)
        self.row_widget.setFixedWidth(len(self.spinner_items) * self.item_width + len(self.spinner_items) * sp.margin)

        for idx, item in enumerate(self.spinner_items, start=0):
            container = QWidget()
            temp_layout = QVBoxLayout(container)
            container.setStyleSheet("background-color: grey")
            container.resize(250, 100) 

            header = QHBoxLayout()

            title = QLabel(f'EDO')
            title.setStyleSheet("font-size: 20px; font-weight: bold; color: white")
            header.addWidget(title)

            copy_item = QPushButton("+")
            copy_item.setStyleSheet("font-size: 18px; color: white")
            copy_item.setFixedWidth(40)
            copy_item.clicked.connect(lambda _, n=idx: self._copy(n))
            header.addWidget(copy_item)

            temp_layout.addLayout(header)

            amount = QLabel(f'{item["amount"]} PLN')
            temp_layout.addWidget(amount)
            # text.setStyleSheet("")

            rate = QLabel(f'{item["rate"]}%')
            temp_layout.addWidget(rate)

            years = QLabel(f'{item["years"]} Years')
            temp_layout.addWidget(years)

            self.spinner_layout.addWidget(container)

    def _copy(self, id):
        self.initial_input.setText(self.spinner_items[id]["amount"])
        self.interest_rate_input.setText(self.spinner_items[id]["rate"])
        self.years_input.setText(self.spinner_items[id]["years"])

    def _calc(self, initial_amount, interest_rate, years, next_rate, type):
        try:
            principal = float(initial_amount)
            rate      = float(interest_rate)
            n_years   = int(years)
            next_rate = float(next_rate)
        except ValueError:
            return
    
        inflation = logic.getInflation(b"2024")
        calc = logic.compound_interest(principal, rate, n_years, next_rate, inflation, type)
        print(floor_to(calc.total * 17, 2), floor_to(calc.profit * 17, 2), floor_to(calc.inflation_lost * 17, 2))

    def _add(self, initial_amount, interest_rate, years):
        self.spinner_items.insert(0, {
            "amount": initial_amount,
            "rate": interest_rate,
            "years": years
        })

        self._update_spinner()

def clear_layout(layout: QLayout):
    """Remove *everything* inside `layout` (widgets + nested layouts)."""
    while layout.count():
        item = layout.takeAt(0)

        w = item.widget()
        if w is not None:               
            w.setParent(None)            
            continue

        child_layout = item.layout()
        if child_layout is not None:     
            clear_layout(child_layout)   
            child_layout.deleteLater()

def getBonds():
    count = ctypes.c_size_t()
    ptr = logic.load_bond_types(ctypes.byref(count))

    n = count.value
    if not ptr:
        raise RuntimeError("load_bond_types failed")

    bonds = ptr[:n]
    return bonds

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()