# -*- coding: utf-8 -*-

from os import remove
from os.path import join, split, dirname
from re import match

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QDialog, QMessageBox

from ....Classes.Material import Material
from ....Classes.ImportMatrixVal import ImportMatrixVal
from ....Classes.ImportMatrixXls import ImportMatrixXls
from ....Functions.load import load_machine_materials, load_matlib, LIB_KEY, MACH_KEY
from ....GUI.Dialog.DMatLib.DMatSetup.DMatSetup import DMatSetup
from ....GUI.Dialog.DMatLib.Gen_DMatLib import Gen_DMatLib


class DMatLib(Gen_DMatLib, QDialog):
    """Material Library Dialog to view and modify material data."""

    # Signal to W_MachineSetup to know that the save popup is needed
    saveNeeded = Signal()
    materialListChanged = Signal()

    def __init__(self, material_dict, machine=None, is_lib_mat=True, selected_id=0):
        """Init the Matlib GUI

        Parameters
        ----------
        self : DMatLib
            a DMatLib object
        material_dict: dict
            Materials dictionary (library + machine)
        machine : Machine
            A Machine object to update
        is_lib_mat : bool
            True: Selected material is part of the Library (False machine)
        selected_id :
            Index of the currently selected material

        Returns
        -------

        """

        # Build the interface according to the .ui file
        QDialog.__init__(self)
        self.setupUi(self)

        self.current_dialog = None  # For DMatSetup popup
        self.is_lib_mat = (
            is_lib_mat  # Current selected mat in is the Library (false machine)
        )
        self.material_dict = material_dict
        self.machine = machine
        self.update_list_mat()

        # Select the material
        self.set_current_material(selected_id, is_lib_mat)

        # Hide since unused
        self.out_epsr.hide()

        # Connect Slot/Signals
        self.nav_mat.clicked.connect(lambda: self.update_out(is_lib_mat=True))
        self.nav_mat.doubleClicked.connect(self.edit_material)

        self.nav_mat_mach.clicked.connect(lambda: self.update_out(is_lib_mat=False))
        self.nav_mat_mach.doubleClicked.connect(self.edit_material)

        self.le_search.textChanged.connect(self.update_list_mat)

        self.b_edit.clicked.connect(self.edit_material)
        self.b_delete.clicked.connect(self.delete_material)
        self.b_duplicate.clicked.connect(self.new_material)

    def get_current_material(self):
        """Return the current selected material"""
        # Get the selected material
        if self.is_lib_mat:
            if self.nav_mat.currentRow() == -1:
                return None, None
            index = self.nav_mat.currentRow()
            return self.material_dict[LIB_KEY][index], index
        else:
            if self.nav_mat_mach.currentRow() == -1:
                return None, None
            index = self.nav_mat_mach.currentRow()
            return self.material_dict[MACH_KEY][index], index

    def set_current_material(self, index, is_lib_mat):
        """Change the current selected material"""
        self.is_lib_mat = is_lib_mat
        # Get the selected material
        if self.is_lib_mat:
            self.nav_mat.setCurrentRow(index)
        else:
            self.nav_mat_mach.setCurrentRow(index)
        self.update_out(is_lib_mat=is_lib_mat)

    def edit_material(self):
        """Open the setup material GUI to edit the current material.
        Changes will be saved to the corresponding material file.

        Parameters
        ----------
        self : DMatLib
            A DMatLib object
        """

        # Close previous window if needed
        if self.current_dialog is not None:
            self.current_dialog.close()

        current_mat, index = self.get_current_material()
        # creates a copy of the material, i.e. self.matlib won't be edited directly
        # is_lib_mat and index to know which Material to update
        self.current_dialog = DMatSetup(current_mat, self.is_lib_mat, index)
        self.current_dialog.finished.connect(self.validate_setup)
        self.current_dialog.show()

    def validate_setup(self, return_code):
        is_lib_mat = self.current_dialog.is_lib_mat
        index = self.current_dialog.index
        mat_edit = self.current_dialog.mat
        init_name = self.current_dialog.init_name
        # Reset dialog
        self.current_dialog = None
        # 0: Cancel, 1: Save, 2: Add to Matlib (from Machine)
        if return_code > 0:
            if return_code == 2:  # Matlib=> machine or machine => Matlib
                if is_lib_mat:  # Library to machine
                    mat_edit.name = mat_edit.name + "_edit"
                    self.material_dict[MACH_KEY].append(mat_edit)
                    index = len(self.material_dict[MACH_KEY]) - 1
                else:
                    index = None  # will be handled as "New material" in Lib
                    mat_edit.path = join(
                        self.material_dict["MATLIB_PATH"], mat_edit.name + ".json"
                    )
                is_lib_mat = not is_lib_mat

            # Update materials in the machine
            if self.machine is not None:
                mach_mat_dict = self.machine.get_material_dict(path="self.machine")
                for mat_path, mach_mat in mach_mat_dict.items():
                    if mach_mat.name == init_name:  # Use original name
                        mat_path_split = mat_path.split(".")
                        setattr(
                            eval(".".join(mat_path_split[:-1])),
                            mat_path_split[-1],
                            mat_edit,
                        )
                        self.saveNeeded.emit()

            if mat_edit.name != init_name and is_lib_mat and index is not None:
                # Renaming a Library material => Delete original one
                remove(join(dirname(mat_edit.path), init_name + ".json"))
                self.material_dict[LIB_KEY][index] = mat_edit
                mat_edit.save(mat_edit.path)
                self.materialListChanged.emit()
            elif is_lib_mat and index is not None:  # Update
                self.material_dict[LIB_KEY][index] = mat_edit
                mat_edit.save(mat_edit.path)
            elif is_lib_mat and index is None:  # New in Library
                self.material_dict[LIB_KEY].append(mat_edit)
                index = len(self.material_dict[LIB_KEY]) - 1
                mat_edit.save(mat_edit.path)
                self.materialListChanged.emit()
            elif not is_lib_mat and index is None:  # New in Machine
                self.material_dict[MACH_KEY].append(mat_edit)
                index = len(self.material_dict[MACH_KEY]) - 1
                self.materialListChanged.emit()
            else:
                self.material_dict[MACH_KEY][index] = mat_edit
                if mat_edit.name != init_name:  # Rename
                    self.materialListChanged.emit()

            # Update machine material (Machine => Lib)
            if return_code == 2 and is_lib_mat:
                load_machine_materials(
                    machine=self.machine, material_dict=self.material_dict
                )
                self.materialListChanged.emit()
            # Update material list
            self.update_list_mat()
            if is_lib_mat:
                self.nav_mat.setCurrentRow(index)
            else:
                self.nav_mat_mach.setCurrentRow(index)
            self.update_out(is_lib_mat=is_lib_mat)

            # Signal set by WMatSelect to update Combobox
            self.accepted.emit()

    def new_material(self):
        """Open the setup material GUI to create a new material according to
        the current material

        Parameters
        ----------
        self :
            A DMatLib object

        Returns
        -------

        """
        # Create new material
        current_mat, _ = self.get_current_material()
        new_mat = current_mat.copy()
        new_mat.name = new_mat.name + "_copy"
        new_mat.path = new_mat.path[:-5] + "_copy.json"
        # Close previous window if needed
        if self.current_dialog is not None:
            self.current_dialog.close()

        # (creates a copy of the material, i.e. self.matlib won't be edited directly)
        self.current_dialog = DMatSetup(new_mat, self.is_lib_mat, index=None)
        self.current_dialog.finished.connect(self.validate_setup)
        self.current_dialog.show()

    def delete_material(self):
        """Delete the selected material from the Library

        Parameters
        ----------
        self : DMatLib
            A DMatLib object
        """
        current_mat, _ = self.get_current_material()

        if current_mat is not None:
            del_msg = "Are you sure you want to delete " + current_mat.name + " ?"
            reply = QMessageBox.question(
                self, "Confirmation", del_msg, QMessageBox.Yes, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                remove(current_mat.path)
                self.material_dict[LIB_KEY].remove(current_mat)
                # Check that material was not part of the machine
                if self.machine is not None:
                    load_machine_materials(
                        machine=self.machine, material_dict=self.material_dict
                    )
                self.update_list_mat()
                if self.nav_mat.count() > 1:
                    self.nav_mat.setCurrentRow(0)
                self.update_out(is_lib_mat=True)  # Delete only for Library mat
                # Signal set by WMatSelect to update Combobox
                self.materialListChanged.emit()

    def update_list_mat(self):
        """Update the list of Material with the current content of MatLib

        Parameters
        ----------
        self :
            A DMatLib object

        Returns
        -------

        """
        material_dict = self.material_dict

        # Filter the material Library
        self.nav_mat.blockSignals(True)
        self.nav_mat.clear()
        for ii, mat in enumerate(material_dict[LIB_KEY]):
            # todo: add new filter
            if self.le_search.text() != "" and not match(
                ".*" + self.le_search.text().lower() + ".*", mat.name.lower()
            ):
                continue
            self.nav_mat.addItem("%03d" % (ii + 1) + " - " + mat.name)
        self.nav_mat.blockSignals(False)

        # Filter the Machine materials
        self.nav_mat_mach.blockSignals(True)
        self.nav_mat_mach.clear()
        for ii, mat in enumerate(material_dict[MACH_KEY]):
            # todo: add new filter
            if self.le_search.text() != "" and not match(
                ".*" + self.le_search.text().lower() + ".*", mat.name.lower()
            ):
                continue
            self.nav_mat_mach.addItem(
                "%03d" % (len(material_dict[LIB_KEY]) + ii + 1) + " - " + mat.name
            )
        self.nav_mat_mach.blockSignals(False)

        # Hide the widget if machine material list is empty
        if len(material_dict[MACH_KEY]) == 0:
            self.in_machine_mat.setVisible(False)
            self.nav_mat_mach.setVisible(False)
        elif not self.in_machine_mat.isVisible():
            self.in_machine_mat.setVisible(True)
            self.nav_mat_mach.setVisible(True)

    def update_out(self, is_lib_mat=True):
        """Update all the output widget for material preview

        Parameters
        ----------
        self : DMatLib
            A DMatLib object
        is_lib_mat : bool
            True display output of current Library mat, else current machine mat
        """

        self.is_lib_mat = is_lib_mat
        mat, _ = self.get_current_material()
        if mat is None:  # No current material
            mat = Material()
            mat._set_None()

        # No possibility to delete machine materials
        if self.is_lib_mat:
            self.b_delete.setEnabled(True)
        else:
            self.b_delete.setEnabled(False)

        # Update Main parameters
        self.out_name.setText(self.tr("name: ") + str(mat.name))
        if mat.is_isotropic:
            self.out_iso.setText(self.tr("type: isotropic"))
        else:
            self.out_iso.setText(self.tr("type: anisotropic"))

        # Update Electrical parameters
        if mat.elec is not None:
            update_text(self.out_rho_elec, "rho", mat.elec.rho, "ohm.m")
            # update_text(self.out_epsr,"epsr",mat.elec.epsr,None)

        # Update Economical parameters
        if mat.eco is not None:
            update_text(self.out_cost_unit, "cost_unit", mat.eco.cost_unit, u"€/kg")

        # Update Thermics parameters
        if mat.HT is not None:
            update_text(self.out_Cp, "Cp", mat.HT.Cp, "W/kg/K")
            update_text(self.out_alpha, "alpha", mat.HT.alpha, None)
            if mat.is_isotropic:
                self.nav_iso_therm.setCurrentIndex(0)
                update_text(self.out_L, "Lambda", mat.HT.lambda_x, "W/K")
            else:
                self.nav_iso_therm.setCurrentIndex(1)
                update_text(self.out_LX, "Lambda X", mat.HT.lambda_x, "W/K")
                update_text(self.out_LY, "Lambda Y", mat.HT.lambda_y, "W/K")
                update_text(self.out_LZ, "Lambda Z", mat.HT.lambda_z, "W/K")

        # Update Structural parameters
        if mat.struct is not None:
            update_text(self.out_rho_meca, "rho", mat.struct.rho, "kg/m^3")
            if mat.is_isotropic:
                self.nav_iso_meca.setCurrentIndex(0)
                update_text(self.out_E, "E", mat.struct.Ex, "Pa")
                update_text(self.out_G, "G", mat.struct.Gxy, "Pa")
                update_text(self.out_nu, "nu", mat.struct.nu_xy, None)
            else:
                self.nav_iso_meca.setCurrentIndex(1)
                update_text(self.out_EX, None, mat.struct.Ex, None)
                update_text(self.out_GXY, None, mat.struct.Gxy, None)
                update_text(self.out_nu_XY, None, mat.struct.nu_xy, None)
                update_text(self.out_EY, None, mat.struct.Ey, None)
                update_text(self.out_GYZ, None, mat.struct.Gyz, None)
                update_text(self.out_nu_YZ, None, mat.struct.nu_yz, None)
                update_text(self.out_EZ, None, mat.struct.Ez, None)
                update_text(self.out_GXZ, None, mat.struct.Gxz, None)
                update_text(self.out_nu_XZ, None, mat.struct.nu_xz, None)

        # Update Magnetics parameters
        if mat.mag is not None:
            update_text(self.out_mur_lin, "mur_lin", mat.mag.mur_lin, None)
            update_text(self.out_Brm20, "Brm20", mat.mag.Brm20, "T")
            update_text(self.out_alpha_Br, "alpha_Br", mat.mag.alpha_Br, None)
            update_text(self.out_wlam, "wlam", mat.mag.Wlam, "m")
            if (
                isinstance(mat.mag.BH_curve, ImportMatrixXls)
                and mat.mag.BH_curve.file_path is not None
            ):
                BH_text = split(mat.mag.BH_curve.file_path)[1]
            elif isinstance(mat.mag.BH_curve, ImportMatrixVal):
                data = mat.mag.BH_curve.get_data()
                shape_str = str(data.shape) if data is not None else "(-,-)"
                BH_text = "Matrix " + shape_str
            else:
                BH_text = "-"
            self.out_BH.setText(BH_text)

    def closeEvent(self, event):
        """Display a message before leaving

        Parameters
        ----------
        self : DMatSetup
            A DMatSetup object
        event :
            The closing event
        """
        # Close popup if needed
        if self.current_dialog is not None:
            self.current_dialog.close()


def update_text(label, name, value, unit):
    """Update a Qlabel with the value if not None

    Parameters
    ----------
    label :
        Qlabel to update
    name :
        Name of the variable
    value :
        Current value of the variable (can be None)
    unit :
        Variable unit (can be None)

    Returns
    -------

    """
    if value is None:
        val = "?"
    else:
        val = str(value)
        if len(val) > 8:
            val = "%1.2e" % value  # formating: 1.23e+08
    if val[-2:] == ".0":  # Remove ".0" sufix
        val = val[:-2]

    if name is None:  # For E, G, nu table
        txt = val
    else:
        if unit is None:
            txt = name + " = " + val
        else:
            txt = name + " = " + val + " [" + unit + "]"
    label.setText(txt)
