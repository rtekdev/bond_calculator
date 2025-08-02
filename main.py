import sys
import ctypes
from src.pylogic.functions import logic, CompoundReturn
from src.pylogic.helpers import floor_to, Settings
import src.pylogic.setup as sp

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QVBoxLayout, QHBoxLayout, QScrollArea, QLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QFrame

class MainWindow(QMainWindow):
    spinner_items = []
    spinner_layout = QHBoxLayout()
    

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

        # Spinner (Future)
        # self._build_spinner(layout)
        
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
        self._res_dialog(
            floor_to(result.total, 2), 
            floor_to(result.profit, 2), 
            floor_to(result.inflation_lost, 2),
            floor_to(result.allInvested, 2),
            result.profit_percent,
            result.lost_percent,
            t_years)
        

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

    def _res_dialog(self, total: float, profit: float, inflation_lost: float, allInvested: float, profit_percent: float, lost_percent: float, total_years: int):
        message = QMessageBox()
        message.setWindowTitle("Response")
        message.setText(
            f"""Overall Profit In Percentage: 
                {floor_to(profit_percent*100, 2)}%\n\nOverall Lost In Percentage: 
                {floor_to(lost_percent*100, 2)}%
            """
        )
        message.setDetailedText(f"Total: {total} PLN\nProfit: {profit} PLN\nInflation Lost: {inflation_lost} PLN\nAll Invested Money: {allInvested} PLN\nTotal Years: {total_years}\n\nLost is based on last year inflation (GUS data)")
        message.setStyleSheet("font-size: 18px")
        message.setFixedWidth(400)
        message.exec()

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