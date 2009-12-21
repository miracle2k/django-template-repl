from jinja2.ext import Extension
from jinja2 import nodes
from template_repl.repl import setup_readline_history, run_shell
from template_repl.utils import pdb_with_context


__all__ = ('repl',)


class REPLExtension(Extension):

    tags = set(['repl'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno

        use_pdb = False
        if not parser.stream.current.type is 'block_end':
            parser.stream.expect('name:pdb')
            use_pdb = True

        return nodes.Output([
            self.call_method('execute', args=[nodes.Const(use_pdb)])]).set_lineno(lineno)

    def execute(self, use_pdb):
        if use_pdb:
            import ipdb
            ipdb.set_trace()
        else:
            setup_readline_history()
            run_shell(locals())
        return ''


repl = REPLExtension  # nicer import name