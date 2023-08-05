"""This module contains the `Mechanical` class."""

from __future__ import absolute_import

from pyaedt.application.Analysis3D import FieldAnalysis3D
from pyaedt.generic.general_methods import generate_unique_name, aedt_exception_handler
from pyaedt.modules.Boundary import BoundaryObject
from collections import OrderedDict


class Mechanical(FieldAnalysis3D, object):
    """Provides the Mechanical application interface.

    Parameters
    ----------
    projectname : str, optional
        Name of the project to select or the full path to the project
        or AEDTZ archive to open.  The default is ``None``, in which
        case an attempt is made to get an active project. If no
        projects are present, an empty project is created.
    designname : str, optional
        Name of the design to select. The default is ``None``, in
        which case an attempt is made to get an active design. If no
        designs are present, an empty design is created.
    solution_type : str, optional
        Solution type to apply to the design. The default is
        ``None``, in which case the default type is applied.
    setup_name : str, optional
        Name of the setup to use as the nominal. The default is
        ``None``, in which case the active setup is used or
        nothing is used.
    specified_version : str, optional
        Version of AEDT to use. The default is ``None``, in which case
        the active version or latest installed version is used.
        This parameter is ignored when Script is launched within AEDT.
    NG : bool, optional
        Whether to launch AEDT in the non-graphical mode. The default
        is``False``, in which case AEDT is launched in the graphical mode.
        This parameter is ignored when Script is launched within AEDT.
    new_desktop_session : bool, optional
        Whether to launch an instance of AEDT in a new thread, even if
        another instance of the ``specified_version`` is active on the
        machine. The default is ``True``. This parameter is ignored when Script is launched within AEDT.
    close_on_exit : bool, optional
        Whether to release AEDT on exit.
    student_version : bool, optional
        Whether to open the AEDT student version. The default is ``False``.
        This parameter is ignored when Script is launched within AEDT.

    Examples
    --------
    Create an instance of Mechanical and connect to an existing
    HFSS design or create a new HFSS design if one does not exist.

    >>> from pyaedt import Mechanical
    >>> aedtapp = Mechanical()

    Create an instance of Mechanical and link to a project named
    ``"projectname"``. If this project does not exist, create one with
    this name.

    >>> aedtapp = Mechanical(projectname)

    Create an instance of Mechanical and link to a design named
    ``"designname"`` in a project named ``"projectname"``.

    >>> aedtapp = Mechanical(projectname,designame)

    Create an instance of Mechanical and open the specified
    project, which is named ``"myfile.aedt"``.

    >>> aedtapp = Mechanical("myfile.aedt")

    Create a ``Desktop on 2021R2`` object and then create an
    ``Mechanical`` object and open the specified project, which is
    named ``"myfile.aedt"``.

    >>> aedtapp = Mechanical(specified_version="2021.2", projectname="myfile.aedt")

    """

    def __init__(
        self,
        projectname=None,
        designname=None,
        solution_type=None,
        setup_name=None,
        specified_version=None,
        non_graphical=False,
        new_desktop_session=False,
        close_on_exit=False,
        student_version=False,
    ):

        FieldAnalysis3D.__init__(
            self,
            "Mechanical",
            projectname,
            designname,
            solution_type,
            setup_name,
            specified_version,
            non_graphical,
            new_desktop_session,
            close_on_exit,
            student_version,
        )

    def __enter__(self):
        return self

    @aedt_exception_handler
    def assign_em_losses(
        self,
        designname="HFSSDesign1",
        setupname="Setup1",
        sweepname="LastAdaptive",
        map_frequency=None,
        surface_objects=[],
        source_project_name=None,
        paramlist=[],
        object_list=[],
    ):
        """Map EM losses to a Mechanical design.

        Parameters
        ----------
        designname : str, optional
            Name of the design of the source mapping. The default is ``"HFSSDesign1"``.
        setupname : str, optional
            Name of the EM setup. The default is ``"Setup1"``.
        sweepname : str, optional
            Name of the EM sweep to use for the mapping. The default is ``"LastAdaptive"``.
        map_frequency : str, optional
            Frequency to map. The default is ``None``. The value must be ``None`` for
            Eigenmode analysis.
        surface_objects : list, optional
            List objects in the source that are metals. The default is ``[]``.
        source_project_name : str, optional
            Name of the source project. The default is ``None``, in which case
            the source from the same project is used.
        paramlist : list, optional
            List of all parameters in the EM to map. The default is ``[]``.
        object_list : list, optional
             The default is ``[]``.

        Returns
        -------

        """
        assert self.solution_type == "Thermal", "This Method works only in Mechanical Structural Solution"

        self.logger.info("Mapping HFSS EM Lossess")
        oName = self.project_name
        if oName == source_project_name or source_project_name is None:
            projname = "This Project*"
        else:
            projname = source_project_name + ".aedt"
        #
        # Generate a list of model objects from the lists made previously and use to map the HFSS losses into Icepak.
        #
        if not object_list:
            allObjects = self.modeler.primitives.object_names
        else:
            allObjects = object_list[:]
        surfaces = surface_objects
        if map_frequency:
            intr = [map_frequency]
        else:
            intr = []

        argparam = OrderedDict({})
        for el in self.available_variations.nominal_w_values_dict:
            argparam[el] = self.available_variations.nominal_w_values_dict[el]

        for el in paramlist:
            argparam[el] = el

        props = OrderedDict(
            {
                "Objects": allObjects,
                "allObjects": False,
                "Project": projname,
                "projname": "ElectronicsDesktop",
                "Design": designname,
                "Soln": setupname + " : " + sweepname,
                "Params": argparam,
                "ForceSourceToSolve": True,
                "PreservePartnerSoln": True,
                "PathRelativeTo": "TargetProject",
            }
        )
        if intr:
            props["Intrinsics"] = intr
            props["SurfaceOnly"] = surfaces

        name = generate_unique_name("EMLoss")
        bound = BoundaryObject(self, name, props, "EMLoss")
        if bound.create():
            self.boundaries.append(bound)
            self.logger.info("EM losses mapped from design %s.", designname)
            return bound
        return False

    @aedt_exception_handler
    def assign_thermal_map(
        self,
        object_list,
        designname="IcepakDesign1",
        setupname="Setup1",
        sweepname="SteadyState",
        source_project_name=None,
        paramlist=[],
    ):
        """Map thermal losses to a Mechanical design.

        .. note::
           This method works in 2021 R2 only when coupled with Icepak.

        Parameters
        ----------
        object_list : list

        designname : str, optional
            Name of the design with the source mapping. The default is ``"IcepakDesign1"``.
        setupname : str, optional
            Name of the EM setup. The default is ``"Setup1"``.
        sweepname :str, optional
            Name of the EM sweep to use for the mapping. The default is ``"SteadyState"``.
        source_project_name : str, optional
            Name of the source project. The default is ``None``, in which case the
            source from the same project is used.
        paramlist : list, optional
            List of all parameters in the EM to map. The default is ``[]``.

        Returns
        -------
        :class:`aedt.modules.Boundary.Boundary object`
            Boundary object.
        """

        assert self.solution_type == "Structural", "This method works only in a Mechanical structural solution."

        self.logger.info("Mapping HFSS EM Lossess")
        oName = self.project_name
        if oName == source_project_name or source_project_name is None:
            projname = "This Project*"
        else:
            projname = source_project_name + ".aedt"
        #
        # Generate a list of model objects from the lists made previously and use to map the HFSS losses into Icepak.
        #
        object_list = self.modeler.convert_to_selections(object_list, True)
        if not object_list:
            allObjects = self.modeler.primitives.object_names
        else:
            allObjects = object_list[:]
        argparam = OrderedDict({})
        for el in self.available_variations.nominal_w_values_dict:
            argparam[el] = self.available_variations.nominal_w_values_dict[el]

        for el in paramlist:
            argparam[el] = el

        props = OrderedDict(
            {
                "Objects": allObjects,
                "Uniform": False,
                "Project": projname,
                "Product": "ElectronicsDesktop",
                "Design": designname,
                "Soln": setupname + " : " + sweepname,
                "Params": argparam,
                "ForceSourceToSolve": True,
                "PreservePartnerSoln": True,
                "PathRelativeTo": "TargetProject",
            }
        )

        name = generate_unique_name("ThermalLink")
        bound = BoundaryObject(self, name, props, "ThermalCondition")
        if bound.create():
            self.boundaries.append(bound)
            self.logger.info("Thermal conditions are mapped from design %s.", designname)
            return bound

        return True

    @aedt_exception_handler
    def assign_uniform_convection(
        self, objects_list, convection_value, convection_unit="w_per_m2kel", temperature="AmbientTemp", boundary_name=""
    ):
        """Assign a uniform convection to the face list.

        Parameters
        ----------
        objects_list : list
            List of objects, faces, or both.
        convection_value : float
            Convection value.
        convection_unit : str, optional
            Units for the convection value. The default is ``"w_per_m2kel"``.
        temperature : str, optional
            Temperature. The default is ``"AmbientTemp"``.
        boundary_name : str, optional
            Name of the boundary. The default is ``""``.

        Returns
        -------
        :class:`aedt.modules.Boundary.Boundary object`
            Boundary object.

        """
        assert self.solution_type == "Thermal", "This method works only in a Mechanical structural solution."

        props = {}
        objects_list = self.modeler._convert_list_to_ids(objects_list)

        if type(objects_list) is list:
            if type(objects_list[0]) is str:
                props["Objects"] = objects_list
            else:
                props["Faces"] = objects_list

        props["Temperature"] = temperature
        props["Uniform"] = True
        props["FilmCoeff"] = str(convection_value) + convection_unit

        if not boundary_name:
            boundary_name = generate_unique_name("Convection")
        bound = BoundaryObject(self, boundary_name, props, "Convection")
        if bound.create():
            self.boundaries.append(bound)
            return bound
        return False

    @aedt_exception_handler
    def assign_uniform_temperature(self, objects_list, temperature="AmbientTemp", boundary_name=""):
        """Assign a uniform temperature boundary.

        .. note::
            This method works only in a Mechanical thermal analysis.

        Parameters
        ----------
        objects_list : list
            List of objects, faces, or both.
        temperature : str, optional.
            Type of the temperature. The default is ``"AmbientTemp"``.
        boundary_name : str, optional
            Name of the boundary. The default is ``""``.

        Returns
        -------
        :class:`aedt.modules.Boundary.Boundary object`
            Boundary object.

        """
        assert self.solution_type == "Thermal", "This method works only in a Mechanical structural analysis."

        props = {}
        objects_list = self.modeler._convert_list_to_ids(objects_list)

        if type(objects_list) is list:
            if type(objects_list[0]) is str:
                props["Objects"] = objects_list
            else:
                props["Faces"] = objects_list

        props["Temperature"] = temperature

        if not boundary_name:
            boundary_name = generate_unique_name("Temp")
        bound = BoundaryObject(self, boundary_name, props, "Temperature")
        if bound.create():
            self.boundaries.append(bound)
            return bound
        return False

    @aedt_exception_handler
    def assign_frictionless_support(self, objects_list, boundary_name=""):
        """Assign a Mechanical frictionless support.

        .. note::
            This method works only in a Mechanical structural analysis.

        Parameters
        ----------
        objects_list : list
            List of faces to apply to the frictionless support.
        boundary_name : str, optional
            Name of the boundary. The default is ``""``.

        Returns
        -------
        :class:`aedt.modules.Boundary.Boundary object`
            Boundary object.

        """

        if not (self.solution_type == "Structural" or self.solution_type == "Modal"):
            self.logger.error("This method works only in Mechanical Structural Solution")
            return False
        props = {}
        objects_list = self.modeler._convert_list_to_ids(objects_list)

        if type(objects_list) is list:
            if type(objects_list[0]) is str:
                props["Objects"] = objects_list
            else:
                props["Faces"] = objects_list

        if not boundary_name:
            boundary_name = generate_unique_name("Temp")
        bound = BoundaryObject(self, boundary_name, props, "Frictionless")
        if bound.create():
            self.boundaries.append(bound)
            return bound
        return False

    @aedt_exception_handler
    def assign_fixed_support(self, objects_list, boundary_name=""):
        """Assign a Mechanical fixed support.

        .. note::
           This method works only in a Mechanical structural analysis.

        Parameters
        ----------
        objects_list : list
            List of faces to apply to the fixed support.
        boundary_name : str, optional
            Name of the boundary. The default is ``""``.

        Returns
        -------
        aedt.modules.Boundary.Boundary
            Boundary object.

        """
        if not (self.solution_type == "Structural" or self.solution_type == "Modal"):
            self.logger.error("This method works only in a Mechanical structural solution.")
            return False
        props = {}
        objects_list = self.modeler._convert_list_to_ids(objects_list)

        if type(objects_list) is list:
            props["Faces"] = objects_list

        if not boundary_name:
            boundary_name = generate_unique_name("Temp")
        bound = BoundaryObject(self, boundary_name, props, "FixedSupport")
        if bound.create():
            self.boundaries.append(bound)
            return bound
        return False

    @property
    def existing_analysis_sweeps(self):
        """Existing analysis sweeps in the design.

        Returns
        -------
        list
            List of existing analysis sweeps.

        """
        setup_list = self.existing_analysis_setups
        sweep_list = []
        for el in setup_list:
            sweep_list.append(el + " : Solution")
        return sweep_list
