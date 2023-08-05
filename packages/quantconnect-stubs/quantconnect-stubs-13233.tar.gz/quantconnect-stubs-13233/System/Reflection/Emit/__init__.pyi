import typing

import System
import System.IO
import System.Reflection
import System.Reflection.Emit

System_Reflection_Emit_Label = typing.Any
System_Reflection_Emit_OpCode = typing.Any


class Label(System.IEquatable[System_Reflection_Emit_Label]):
    """This class has no documentation."""

    @property
    def m_label(self) -> int:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def Equals(self, obj: System.Reflection.Emit.Label) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class FlowControl(System.Enum):
    """This class has no documentation."""

    Branch = 0

    Break = 1

    Call = 2

    Cond_Branch = 3

    Meta = 4

    Next = 5

    Phi = 6
    """FlowControl.Phi has been deprecated and is not supported."""

    Return = 7

    Throw = 8


class AssemblyBuilder(System.Reflection.Assembly):
    """This class has no documentation."""

    @property
    def CodeBase(self) -> str:
        ...

    @property
    def Location(self) -> str:
        ...

    @property
    def EntryPoint(self) -> System.Reflection.MethodInfo:
        ...

    @property
    def IsDynamic(self) -> bool:
        ...

    def GetExportedTypes(self) -> typing.List[typing.Type]:
        ...

    def GetFile(self, name: str) -> System.IO.FileStream:
        ...

    def GetFiles(self, getResourceModules: bool) -> typing.List[System.IO.FileStream]:
        ...

    def GetManifestResourceInfo(self, resourceName: str) -> System.Reflection.ManifestResourceInfo:
        ...

    def GetManifestResourceNames(self) -> typing.List[str]:
        ...

    @typing.overload
    def GetManifestResourceStream(self, name: str) -> System.IO.Stream:
        ...

    @typing.overload
    def GetManifestResourceStream(self, type: typing.Type, name: str) -> System.IO.Stream:
        ...


class StackBehaviour(System.Enum):
    """This class has no documentation."""

    Pop0 = 0

    Pop1 = 1

    Pop1_pop1 = 2

    Popi = 3

    Popi_pop1 = 4

    Popi_popi = 5

    Popi_popi8 = 6

    Popi_popi_popi = 7

    Popi_popr4 = 8

    Popi_popr8 = 9

    Popref = 10

    Popref_pop1 = 11

    Popref_popi = 12

    Popref_popi_popi = 13

    Popref_popi_popi8 = 14

    Popref_popi_popr4 = 15

    Popref_popi_popr8 = 16

    Popref_popi_popref = 17

    Push0 = 18

    Push1 = 19

    Push1_push1 = 20

    Pushi = 21

    Pushi8 = 22

    Pushr4 = 23

    Pushr8 = 24

    Pushref = 25

    Varpop = 26

    Varpush = 27

    Popref_popi_pop1 = 28


class PackingSize(System.Enum):
    """This class has no documentation."""

    Unspecified = 0

    Size1 = 1

    Size2 = 2

    Size4 = 4

    Size8 = 8

    Size16 = 16

    Size32 = 32

    Size64 = 64

    Size128 = 128


class OperandType(System.Enum):
    """This class has no documentation."""

    InlineBrTarget = 0

    InlineField = 1

    InlineI = 2

    InlineI8 = 3

    InlineMethod = 4

    InlineNone = 5

    InlinePhi = 6
    """OperandType.InlinePhi has been deprecated and is not supported."""

    InlineR = 7

    InlineSig = 9

    InlineString = 10

    InlineSwitch = 11

    InlineTok = 12

    InlineType = 13

    InlineVar = 14

    ShortInlineBrTarget = 15

    ShortInlineI = 16

    ShortInlineR = 17

    ShortInlineVar = 18


class OpCodeType(System.Enum):
    """This class has no documentation."""

    Annotation = 0
    """OpCodeType.Annotation has been deprecated and is not supported."""

    Macro = 1

    Nternal = 2

    Objmodel = 3

    Prefix = 4

    Primitive = 5


class AssemblyBuilderAccess(System.Enum):
    """This class has no documentation."""

    Run = 1

    RunAndCollect = ...


class PEFileKinds(System.Enum):
    """This class has no documentation."""

    Dll = ...

    ConsoleApplication = ...

    WindowApplication = ...


class OpCode(System.IEquatable[System_Reflection_Emit_OpCode]):
    """This class has no documentation."""

    OperandTypeMask: int = ...

    FlowControlShift: int = 5

    FlowControlMask: int = ...

    OpCodeTypeShift: int = 9

    OpCodeTypeMask: int = ...

    StackBehaviourPopShift: int = 12

    StackBehaviourPushShift: int = 17

    StackBehaviourMask: int = ...

    SizeShift: int = 22

    SizeMask: int = ...

    EndsUncondJmpBlkFlag: int = ...

    StackChangeShift: int = 28

    @property
    def OperandType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.OperandType enum."""
        ...

    @property
    def FlowControl(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.FlowControl enum."""
        ...

    @property
    def OpCodeType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.OpCodeType enum."""
        ...

    @property
    def StackBehaviourPop(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.StackBehaviour enum."""
        ...

    @property
    def StackBehaviourPush(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.StackBehaviour enum."""
        ...

    @property
    def Size(self) -> int:
        ...

    @property
    def Value(self) -> int:
        ...

    @property
    def Name(self) -> str:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def Equals(self, obj: System.Reflection.Emit.OpCode) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        ...


class OpCodes(System.Object):
    """
    The IL instruction opcodes supported by the
          runtime. The IL Instruction Specification describes each
          Opcode.
    """

    Nop: System.Reflection.Emit.OpCode = ...

    Break: System.Reflection.Emit.OpCode = ...

    Ldarg_0: System.Reflection.Emit.OpCode = ...

    Ldarg_1: System.Reflection.Emit.OpCode = ...

    Ldarg_2: System.Reflection.Emit.OpCode = ...

    Ldarg_3: System.Reflection.Emit.OpCode = ...

    Ldloc_0: System.Reflection.Emit.OpCode = ...

    Ldloc_1: System.Reflection.Emit.OpCode = ...

    Ldloc_2: System.Reflection.Emit.OpCode = ...

    Ldloc_3: System.Reflection.Emit.OpCode = ...

    Stloc_0: System.Reflection.Emit.OpCode = ...

    Stloc_1: System.Reflection.Emit.OpCode = ...

    Stloc_2: System.Reflection.Emit.OpCode = ...

    Stloc_3: System.Reflection.Emit.OpCode = ...

    Ldarg_S: System.Reflection.Emit.OpCode = ...

    Ldarga_S: System.Reflection.Emit.OpCode = ...

    Starg_S: System.Reflection.Emit.OpCode = ...

    Ldloc_S: System.Reflection.Emit.OpCode = ...

    Ldloca_S: System.Reflection.Emit.OpCode = ...

    Stloc_S: System.Reflection.Emit.OpCode = ...

    Ldnull: System.Reflection.Emit.OpCode = ...

    Ldc_I4_M1: System.Reflection.Emit.OpCode = ...

    Ldc_I4_0: System.Reflection.Emit.OpCode = ...

    Ldc_I4_1: System.Reflection.Emit.OpCode = ...

    Ldc_I4_2: System.Reflection.Emit.OpCode = ...

    Ldc_I4_3: System.Reflection.Emit.OpCode = ...

    Ldc_I4_4: System.Reflection.Emit.OpCode = ...

    Ldc_I4_5: System.Reflection.Emit.OpCode = ...

    Ldc_I4_6: System.Reflection.Emit.OpCode = ...

    Ldc_I4_7: System.Reflection.Emit.OpCode = ...

    Ldc_I4_8: System.Reflection.Emit.OpCode = ...

    Ldc_I4_S: System.Reflection.Emit.OpCode = ...

    Ldc_I4: System.Reflection.Emit.OpCode = ...

    Ldc_I8: System.Reflection.Emit.OpCode = ...

    Ldc_R4: System.Reflection.Emit.OpCode = ...

    Ldc_R8: System.Reflection.Emit.OpCode = ...

    Dup: System.Reflection.Emit.OpCode = ...

    Pop: System.Reflection.Emit.OpCode = ...

    Jmp: System.Reflection.Emit.OpCode = ...

    Call: System.Reflection.Emit.OpCode = ...

    Calli: System.Reflection.Emit.OpCode = ...

    Ret: System.Reflection.Emit.OpCode = ...

    Br_S: System.Reflection.Emit.OpCode = ...

    Brfalse_S: System.Reflection.Emit.OpCode = ...

    Brtrue_S: System.Reflection.Emit.OpCode = ...

    Beq_S: System.Reflection.Emit.OpCode = ...

    Bge_S: System.Reflection.Emit.OpCode = ...

    Bgt_S: System.Reflection.Emit.OpCode = ...

    Ble_S: System.Reflection.Emit.OpCode = ...

    Blt_S: System.Reflection.Emit.OpCode = ...

    Bne_Un_S: System.Reflection.Emit.OpCode = ...

    Bge_Un_S: System.Reflection.Emit.OpCode = ...

    Bgt_Un_S: System.Reflection.Emit.OpCode = ...

    Ble_Un_S: System.Reflection.Emit.OpCode = ...

    Blt_Un_S: System.Reflection.Emit.OpCode = ...

    Br: System.Reflection.Emit.OpCode = ...

    Brfalse: System.Reflection.Emit.OpCode = ...

    Brtrue: System.Reflection.Emit.OpCode = ...

    Beq: System.Reflection.Emit.OpCode = ...

    Bge: System.Reflection.Emit.OpCode = ...

    Bgt: System.Reflection.Emit.OpCode = ...

    Ble: System.Reflection.Emit.OpCode = ...

    Blt: System.Reflection.Emit.OpCode = ...

    Bne_Un: System.Reflection.Emit.OpCode = ...

    Bge_Un: System.Reflection.Emit.OpCode = ...

    Bgt_Un: System.Reflection.Emit.OpCode = ...

    Ble_Un: System.Reflection.Emit.OpCode = ...

    Blt_Un: System.Reflection.Emit.OpCode = ...

    Switch: System.Reflection.Emit.OpCode = ...

    Ldind_I1: System.Reflection.Emit.OpCode = ...

    Ldind_U1: System.Reflection.Emit.OpCode = ...

    Ldind_I2: System.Reflection.Emit.OpCode = ...

    Ldind_U2: System.Reflection.Emit.OpCode = ...

    Ldind_I4: System.Reflection.Emit.OpCode = ...

    Ldind_U4: System.Reflection.Emit.OpCode = ...

    Ldind_I8: System.Reflection.Emit.OpCode = ...

    Ldind_I: System.Reflection.Emit.OpCode = ...

    Ldind_R4: System.Reflection.Emit.OpCode = ...

    Ldind_R8: System.Reflection.Emit.OpCode = ...

    Ldind_Ref: System.Reflection.Emit.OpCode = ...

    Stind_Ref: System.Reflection.Emit.OpCode = ...

    Stind_I1: System.Reflection.Emit.OpCode = ...

    Stind_I2: System.Reflection.Emit.OpCode = ...

    Stind_I4: System.Reflection.Emit.OpCode = ...

    Stind_I8: System.Reflection.Emit.OpCode = ...

    Stind_R4: System.Reflection.Emit.OpCode = ...

    Stind_R8: System.Reflection.Emit.OpCode = ...

    Add: System.Reflection.Emit.OpCode = ...

    Sub: System.Reflection.Emit.OpCode = ...

    Mul: System.Reflection.Emit.OpCode = ...

    Div: System.Reflection.Emit.OpCode = ...

    Div_Un: System.Reflection.Emit.OpCode = ...

    Rem: System.Reflection.Emit.OpCode = ...

    Rem_Un: System.Reflection.Emit.OpCode = ...

    And: System.Reflection.Emit.OpCode = ...

    Or: System.Reflection.Emit.OpCode = ...

    Xor: System.Reflection.Emit.OpCode = ...

    Shl: System.Reflection.Emit.OpCode = ...

    Shr: System.Reflection.Emit.OpCode = ...

    Shr_Un: System.Reflection.Emit.OpCode = ...

    Neg: System.Reflection.Emit.OpCode = ...

    Not: System.Reflection.Emit.OpCode = ...

    Conv_I1: System.Reflection.Emit.OpCode = ...

    Conv_I2: System.Reflection.Emit.OpCode = ...

    Conv_I4: System.Reflection.Emit.OpCode = ...

    Conv_I8: System.Reflection.Emit.OpCode = ...

    Conv_R4: System.Reflection.Emit.OpCode = ...

    Conv_R8: System.Reflection.Emit.OpCode = ...

    Conv_U4: System.Reflection.Emit.OpCode = ...

    Conv_U8: System.Reflection.Emit.OpCode = ...

    Callvirt: System.Reflection.Emit.OpCode = ...

    Cpobj: System.Reflection.Emit.OpCode = ...

    Ldobj: System.Reflection.Emit.OpCode = ...

    Ldstr: System.Reflection.Emit.OpCode = ...

    Newobj: System.Reflection.Emit.OpCode = ...

    Castclass: System.Reflection.Emit.OpCode = ...

    Isinst: System.Reflection.Emit.OpCode = ...

    Conv_R_Un: System.Reflection.Emit.OpCode = ...

    Unbox: System.Reflection.Emit.OpCode = ...

    Throw: System.Reflection.Emit.OpCode = ...

    Ldfld: System.Reflection.Emit.OpCode = ...

    Ldflda: System.Reflection.Emit.OpCode = ...

    Stfld: System.Reflection.Emit.OpCode = ...

    Ldsfld: System.Reflection.Emit.OpCode = ...

    Ldsflda: System.Reflection.Emit.OpCode = ...

    Stsfld: System.Reflection.Emit.OpCode = ...

    Stobj: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I1_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I2_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I4_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I8_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U1_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U2_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U4_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U8_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U_Un: System.Reflection.Emit.OpCode = ...

    Box: System.Reflection.Emit.OpCode = ...

    Newarr: System.Reflection.Emit.OpCode = ...

    Ldlen: System.Reflection.Emit.OpCode = ...

    Ldelema: System.Reflection.Emit.OpCode = ...

    Ldelem_I1: System.Reflection.Emit.OpCode = ...

    Ldelem_U1: System.Reflection.Emit.OpCode = ...

    Ldelem_I2: System.Reflection.Emit.OpCode = ...

    Ldelem_U2: System.Reflection.Emit.OpCode = ...

    Ldelem_I4: System.Reflection.Emit.OpCode = ...

    Ldelem_U4: System.Reflection.Emit.OpCode = ...

    Ldelem_I8: System.Reflection.Emit.OpCode = ...

    Ldelem_I: System.Reflection.Emit.OpCode = ...

    Ldelem_R4: System.Reflection.Emit.OpCode = ...

    Ldelem_R8: System.Reflection.Emit.OpCode = ...

    Ldelem_Ref: System.Reflection.Emit.OpCode = ...

    Stelem_I: System.Reflection.Emit.OpCode = ...

    Stelem_I1: System.Reflection.Emit.OpCode = ...

    Stelem_I2: System.Reflection.Emit.OpCode = ...

    Stelem_I4: System.Reflection.Emit.OpCode = ...

    Stelem_I8: System.Reflection.Emit.OpCode = ...

    Stelem_R4: System.Reflection.Emit.OpCode = ...

    Stelem_R8: System.Reflection.Emit.OpCode = ...

    Stelem_Ref: System.Reflection.Emit.OpCode = ...

    Ldelem: System.Reflection.Emit.OpCode = ...

    Stelem: System.Reflection.Emit.OpCode = ...

    Unbox_Any: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I1: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U1: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I2: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U2: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I4: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U4: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I8: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U8: System.Reflection.Emit.OpCode = ...

    Refanyval: System.Reflection.Emit.OpCode = ...

    Ckfinite: System.Reflection.Emit.OpCode = ...

    Mkrefany: System.Reflection.Emit.OpCode = ...

    Ldtoken: System.Reflection.Emit.OpCode = ...

    Conv_U2: System.Reflection.Emit.OpCode = ...

    Conv_U1: System.Reflection.Emit.OpCode = ...

    Conv_I: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U: System.Reflection.Emit.OpCode = ...

    Add_Ovf: System.Reflection.Emit.OpCode = ...

    Add_Ovf_Un: System.Reflection.Emit.OpCode = ...

    Mul_Ovf: System.Reflection.Emit.OpCode = ...

    Mul_Ovf_Un: System.Reflection.Emit.OpCode = ...

    Sub_Ovf: System.Reflection.Emit.OpCode = ...

    Sub_Ovf_Un: System.Reflection.Emit.OpCode = ...

    Endfinally: System.Reflection.Emit.OpCode = ...

    Leave: System.Reflection.Emit.OpCode = ...

    Leave_S: System.Reflection.Emit.OpCode = ...

    Stind_I: System.Reflection.Emit.OpCode = ...

    Conv_U: System.Reflection.Emit.OpCode = ...

    Prefix7: System.Reflection.Emit.OpCode = ...

    Prefix6: System.Reflection.Emit.OpCode = ...

    Prefix5: System.Reflection.Emit.OpCode = ...

    Prefix4: System.Reflection.Emit.OpCode = ...

    Prefix3: System.Reflection.Emit.OpCode = ...

    Prefix2: System.Reflection.Emit.OpCode = ...

    Prefix1: System.Reflection.Emit.OpCode = ...

    Prefixref: System.Reflection.Emit.OpCode = ...

    Arglist: System.Reflection.Emit.OpCode = ...

    Ceq: System.Reflection.Emit.OpCode = ...

    Cgt: System.Reflection.Emit.OpCode = ...

    Cgt_Un: System.Reflection.Emit.OpCode = ...

    Clt: System.Reflection.Emit.OpCode = ...

    Clt_Un: System.Reflection.Emit.OpCode = ...

    Ldftn: System.Reflection.Emit.OpCode = ...

    Ldvirtftn: System.Reflection.Emit.OpCode = ...

    Ldarg: System.Reflection.Emit.OpCode = ...

    Ldarga: System.Reflection.Emit.OpCode = ...

    Starg: System.Reflection.Emit.OpCode = ...

    Ldloc: System.Reflection.Emit.OpCode = ...

    Ldloca: System.Reflection.Emit.OpCode = ...

    Stloc: System.Reflection.Emit.OpCode = ...

    Localloc: System.Reflection.Emit.OpCode = ...

    Endfilter: System.Reflection.Emit.OpCode = ...

    Unaligned: System.Reflection.Emit.OpCode = ...

    Volatile: System.Reflection.Emit.OpCode = ...

    Tailcall: System.Reflection.Emit.OpCode = ...

    Initobj: System.Reflection.Emit.OpCode = ...

    Constrained: System.Reflection.Emit.OpCode = ...

    Cpblk: System.Reflection.Emit.OpCode = ...

    Initblk: System.Reflection.Emit.OpCode = ...

    Rethrow: System.Reflection.Emit.OpCode = ...

    Sizeof: System.Reflection.Emit.OpCode = ...

    Refanytype: System.Reflection.Emit.OpCode = ...

    Readonly: System.Reflection.Emit.OpCode = ...

    @staticmethod
    def TakesSingleByteArgument(inst: System.Reflection.Emit.OpCode) -> bool:
        ...


class LocalBuilder(System.Reflection.LocalVariableInfo):
    """This class has no documentation."""

    @property
    def type(self) -> typing.Type:
        ...

    @type.setter
    def type(self, value: typing.Type):
        ...

    @property
    def is_pinned(self) -> bool:
        ...

    @is_pinned.setter
    def is_pinned(self, value: bool):
        ...

    @property
    def position(self) -> int:
        ...

    @position.setter
    def position(self, value: int):
        ...

    @property
    def ilgen(self) -> System.Reflection.Emit.ILGenerator:
        ...

    @ilgen.setter
    def ilgen(self, value: System.Reflection.Emit.ILGenerator):
        ...

    @property
    def LocalType(self) -> typing.Type:
        ...

    @property
    def IsPinned(self) -> bool:
        ...

    @property
    def LocalIndex(self) -> int:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def StartOffset(self) -> int:
        ...

    @property
    def EndOffset(self) -> int:
        ...


