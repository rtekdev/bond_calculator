import sys
import ctypes
from src.pylogic.functions import logic, CompoundReturn
from src.pylogic.helpers import floor_to, Settings
import src.pylogic.setup as sp

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QScrollArea, QLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QFrame

class MainWindow(QMainWindow):
    spinner_items = []
    spinner_layout = QHBoxLayout()
    item_width = 250

    # settings
    # 0 - Auto
    # 1 - Manual
    bond_offers = Settings(0)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super BOND Calculator")
        
        layout = QVBoxLayout()
        self._build_components(layout) 
        layout.addStretch()

        self._build_spinner(layout)
        
        
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.resize(sp.width, sp.height)

    def _build_components(self, layout: QLayout):
        title = QLabel("Super BOND calculator")
        title.setStyleSheet("font-size: 24px; color: white; font-weight: bold")
        title.setMargin(10)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)

        container = QHBoxLayout()

        # First Column
        firstColumn = QVBoxLayout()

        self.initial_input = self._create_num_line_edit("Enter initial amount (26000)", firstColumn)
        self.interest_rate_input = self._create_num_line_edit("Enter interest rate (6.25%)", firstColumn)
        self.years_input = self._create_num_line_edit("Enter BOND's years (10)", firstColumn)

        # Third Column
        # Bond below 10 years / settings

        secondColumn = QVBoxLayout()

        total_years_input = self._create_num_line_edit("Total years", secondColumn)
        regular_amount_input = self._create_num_line_edit("Regular amount payment", secondColumn)
        
        regular_type_input = QComboBox()
        regular_type_input.addItems(['yearly', 'monthly'])
        regular_type_input.setStyleSheet("font-size: 18px; padding: 4px 8px; margin: 5px")
        secondColumn.addWidget(regular_type_input)

        # Third Column
        thirdColumn = QVBoxLayout()

        choose_bond = self._build_combo_box()
        thirdColumn.addWidget(choose_bond)

        self.type_combo = QComboBox()
        self.type_combo.addItems(['inflation', 'permanent'])
        self.type_combo.setStyleSheet("font-size: 18px; padding: 4px 8px; margin: 5px")
        thirdColumn.addWidget(self.type_combo)

        self.next_rate_input = self._create_num_line_edit("Next rate (2%)", thirdColumn)

        

        # Controls
        controls = QHBoxLayout()

        button_add = QPushButton("Add")
        button_add.setStyleSheet(sp.input_styles)
        button_add.clicked.connect(lambda: self._add(self.initial_input.text(), self.interest_rate_input.text(), self.years_input.text()))
        controls.addWidget(button_add)

        button_calc = QPushButton("Calculate")
        button_calc.setStyleSheet(f"{sp.input_styles}; background-color: green")
        button_calc.clicked.connect(
            lambda: self._calc(
                self.initial_input.text(), 
                self.interest_rate_input.text(), 
                self.years_input.text(), 
                self.next_rate_input.text(), 
                self.type_combo.currentText(),
                total_years_input.text(),
                regular_amount_input.text(),
                regular_type_input.currentText()
            ))
        controls.addWidget(button_calc)

        container.addLayout(firstColumn)
        container.addLayout(secondColumn)
        container.addLayout(thirdColumn)
        
        layout.addLayout(container)
        layout.addLayout(controls)

    def _build_combo_box(self):
        combo = QComboBox()
        combo.setStyleSheet("font-size: 18px; padding: 4px 8px; margin: 5px")
        
        bonds = getBonds()
        combo.addItem('Custom')
        for item in bonds:
            combo.addItem(item["name"])

        combo.currentTextChanged.connect(self._update_combo)

        return combo

    def _update_combo(self, name):
    
        bonds = getBonds()
        names = [item["name"] for item in bonds]

        try:
            idx = names.index(name)
            self.interest_rate_input.setText(str(bonds[idx]["interest_rate"]))
            self.years_input.setText(str(bonds[idx]["years"]))
            self.next_rate_input.setText(str(bonds[idx]["next_rate"]))
            self.type_combo.setCurrentText(str(bonds[idx]["type"]))
            self.next_rate_input.setEnabled(False)
            self.type_combo.setEnabled(False)
                
        except ValueError:
            if name.__eq__('Custom'):
                self.next_rate_input.setEnabled(True)
                self.type_combo.setEnabled(True)
            else:
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

    def _calc(self, initial_amount, interest_rate, years, next_rate, type, total_years, regular_amount, regular_type):
        try:
            principal = float(initial_amount)
            rate      = float(interest_rate)
            n_years   = int(years)
            nrate     = float(next_rate)
            t_years   = int(total_years)
            r_amount  = float(regular_amount)
        except ValueError:
            return
    
        inflation = logic.getInflation(b"2024")
        result = CompoundReturn()
        logic.compound_interest(
            ctypes.byref(result),
            principal,
            rate,
            n_years,
            nrate,
            inflation,
            type.encode("ascii"),
            t_years,
            r_amount,
            regular_type.encode("ascii")
        )
        print(floor_to(result.total, 2), floor_to(result.profit, 2), floor_to(result.inflation_lost * 17, 2))

    def _add(self, initial_amount, interest_rate, years):
        self.spinner_items.insert(0, {
            "amount": initial_amount,
            "rate": interest_rate,
            "years": years
        })

        self._update_spinner()

    def _create_num_line_edit(self, placeholder: str, layout: QLayout): 
        input = QLineEdit()
        input.setPlaceholderText(placeholder)
        input.setStyleSheet(sp.input_styles)
        layout.addWidget(input)

        return input

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
    count = ctypes.c_int()
    ptr = logic.getBonds(ctypes.byref(count))
    if not ptr:
        raise RuntimeError("getBonds failed")

    bonds = []
    for i in range(count.value):
        b = ptr[i]
        bonds.append({
            "name": b.name.decode(),
            "years": b.years,
            "interest_rate": b.interest_rate,
            "next_rate": b.next_rate,
            "type": b.type.decode(),
        })

    logic.freeBonds(ptr, count.value)

    return bonds

getBonds()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()