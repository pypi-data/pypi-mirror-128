# Generated from agbpycc/ASM.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ASMParser import ASMParser
else:
    from ASMParser import ASMParser

# This class defines a complete generic visitor for a parse tree produced by ASMParser.

class ASMVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ASMParser#asmfile.
    def visitAsmfile(self, ctx:ASMParser.AsmfileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#function.
    def visitFunction(self, ctx:ASMParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#function_header.
    def visitFunction_header(self, ctx:ASMParser.Function_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#function_header1.
    def visitFunction_header1(self, ctx:ASMParser.Function_header1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#function_header2.
    def visitFunction_header2(self, ctx:ASMParser.Function_header2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#line.
    def visitLine(self, ctx:ASMParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#label.
    def visitLabel(self, ctx:ASMParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#instruction.
    def visitInstruction(self, ctx:ASMParser.InstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#push.
    def visitPush(self, ctx:ASMParser.PushContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#push_multiple.
    def visitPush_multiple(self, ctx:ASMParser.Push_multipleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#pop.
    def visitPop(self, ctx:ASMParser.PopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#pop_multiple.
    def visitPop_multiple(self, ctx:ASMParser.Pop_multipleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#arithmetic.
    def visitArithmetic(self, ctx:ASMParser.ArithmeticContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#add.
    def visitAdd(self, ctx:ASMParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#sub.
    def visitSub(self, ctx:ASMParser.SubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#mul.
    def visitMul(self, ctx:ASMParser.MulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#mul1.
    def visitMul1(self, ctx:ASMParser.Mul1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#mul2.
    def visitMul2(self, ctx:ASMParser.Mul2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#rsb.
    def visitRsb(self, ctx:ASMParser.RsbContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#neg.
    def visitNeg(self, ctx:ASMParser.NegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#logic.
    def visitLogic(self, ctx:ASMParser.LogicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#land.
    def visitLand(self, ctx:ASMParser.LandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#orr.
    def visitOrr(self, ctx:ASMParser.OrrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#eor.
    def visitEor(self, ctx:ASMParser.EorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#lsl.
    def visitLsl(self, ctx:ASMParser.LslContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#lsr.
    def visitLsr(self, ctx:ASMParser.LsrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#asl.
    def visitAsl(self, ctx:ASMParser.AslContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#asr.
    def visitAsr(self, ctx:ASMParser.AsrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bic.
    def visitBic(self, ctx:ASMParser.BicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#mov.
    def visitMov(self, ctx:ASMParser.MovContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#mvn.
    def visitMvn(self, ctx:ASMParser.MvnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#branch.
    def visitBranch(self, ctx:ASMParser.BranchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#b.
    def visitB(self, ctx:ASMParser.BContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bl.
    def visitBl(self, ctx:ASMParser.BlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bx.
    def visitBx(self, ctx:ASMParser.BxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#beq.
    def visitBeq(self, ctx:ASMParser.BeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bne.
    def visitBne(self, ctx:ASMParser.BneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bhs.
    def visitBhs(self, ctx:ASMParser.BhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#blo.
    def visitBlo(self, ctx:ASMParser.BloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bmi.
    def visitBmi(self, ctx:ASMParser.BmiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bpl.
    def visitBpl(self, ctx:ASMParser.BplContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bvs.
    def visitBvs(self, ctx:ASMParser.BvsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bvc.
    def visitBvc(self, ctx:ASMParser.BvcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bhi.
    def visitBhi(self, ctx:ASMParser.BhiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bls.
    def visitBls(self, ctx:ASMParser.BlsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bge.
    def visitBge(self, ctx:ASMParser.BgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#blt.
    def visitBlt(self, ctx:ASMParser.BltContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#bgt.
    def visitBgt(self, ctx:ASMParser.BgtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#ble.
    def visitBle(self, ctx:ASMParser.BleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#ldr.
    def visitLdr(self, ctx:ASMParser.LdrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#ldr_pc.
    def visitLdr_pc(self, ctx:ASMParser.Ldr_pcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#ldr_offset.
    def visitLdr_offset(self, ctx:ASMParser.Ldr_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#ldrh_offset.
    def visitLdrh_offset(self, ctx:ASMParser.Ldrh_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#ldrsh_offset.
    def visitLdrsh_offset(self, ctx:ASMParser.Ldrsh_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#ldrb_offset.
    def visitLdrb_offset(self, ctx:ASMParser.Ldrb_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#ldrsb_offset.
    def visitLdrsb_offset(self, ctx:ASMParser.Ldrsb_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#store.
    def visitStore(self, ctx:ASMParser.StoreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#str_offset.
    def visitStr_offset(self, ctx:ASMParser.Str_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#strh_offset.
    def visitStrh_offset(self, ctx:ASMParser.Strh_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#strb_offset.
    def visitStrb_offset(self, ctx:ASMParser.Strb_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#stm.
    def visitStm(self, ctx:ASMParser.StmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#cmp.
    def visitCmp(self, ctx:ASMParser.CmpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#cmn.
    def visitCmn(self, ctx:ASMParser.CmnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#directive.
    def visitDirective(self, ctx:ASMParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#align.
    def visitAlign(self, ctx:ASMParser.AlignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#dir_code.
    def visitDir_code(self, ctx:ASMParser.Dir_codeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#dir_gcc.
    def visitDir_gcc(self, ctx:ASMParser.Dir_gccContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#dir_size.
    def visitDir_size(self, ctx:ASMParser.Dir_sizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#dir_file.
    def visitDir_file(self, ctx:ASMParser.Dir_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#dir_loc.
    def visitDir_loc(self, ctx:ASMParser.Dir_locContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#data.
    def visitData(self, ctx:ASMParser.DataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#data1word.
    def visitData1word(self, ctx:ASMParser.Data1wordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#data2word.
    def visitData2word(self, ctx:ASMParser.Data2wordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#data4word.
    def visitData4word(self, ctx:ASMParser.Data4wordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#data1num.
    def visitData1num(self, ctx:ASMParser.Data1numContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#data2num.
    def visitData2num(self, ctx:ASMParser.Data2numContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#data4num.
    def visitData4num(self, ctx:ASMParser.Data4numContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#include.
    def visitInclude(self, ctx:ASMParser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#syntax.
    def visitSyntax(self, ctx:ASMParser.SyntaxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#reglist.
    def visitReglist(self, ctx:ASMParser.ReglistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#regimm.
    def visitRegimm(self, ctx:ASMParser.RegimmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#reg.
    def visitReg(self, ctx:ASMParser.RegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASMParser#imm.
    def visitImm(self, ctx:ASMParser.ImmContext):
        return self.visitChildren(ctx)



del ASMParser