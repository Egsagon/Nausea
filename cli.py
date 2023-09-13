import os
import glob
import time
import click
import macro
import pickle

@click.group
def cli(): pass

@cli.command
@click.option('-d', '--delay', help = 'Time delay before recording', default = '3')
@click.option('-n', '--name', help = 'Macro name', default = 'macro')
def record(delay: str, name: str) -> None:
    '''
    Record keys.
    '''
    
    # Delay
    if delay and delay.isdigit():
        delay = int(delay)
    
    else: delay = 0
    
    print()
    for i in range(delay):
        print(f'\rStarting record in \033[91m{delay - i: >4}', end = '\033[0m')
        time.sleep(1)
    
    t_size = os.get_terminal_size().columns
    
    print(f'\r\033[91m{"*** recording ***": ^{t_size}}\033[0m')
    
    def stopper(event) -> None:
        return event == macro.key.f8
    
    def on_event(event) -> None:
        print(f'[ + ] New entry: \033[93m{event[2]} \033[92m{event[3]}\033[0m')
    
    def on_done(events) -> None:
        print(f'\r\033[91m{"*** End record ***": ^{t_size}}\033[0m')
        
        # Save macro
        with open(f'{name}.vomit', 'wb') as file:
            file.write(pickle.dumps(events))
        
        print(f'\nMacro saved as \033[92m{name}\033[0m.vomit!')
        
        runner.stop()
    
    runner = macro.Runner()
    runner.record(stopper, on_event, on_done)
    runner.block()

@cli.command
def macros() -> None:
    '''
    List saved macros.
    '''
    
    files = glob.glob('*.vomit')
    t_size = os.get_terminal_size().columns

    title = f' Found {len(files)} macros '
    print(f'{title:-^{t_size}}')
    
    for file in files:
        
        with open(file, 'rb') as raw:
            event_list = pickle.load(raw)
        
        print(f'\033[92m{file: <30}\033[0m | \033[93m{len(event_list)}\033[0m entries')
    
    print('-' * t_size)

@cli.command
@click.option('-n', '--name', help = 'Macro filename or path without extension')
@click.option('-c', '--count', help = 'Number of iterations', default = '1')
@click.option('-d', '--delay', help = 'Delay before starting the macro', default = '3')
@click.option('-ld', '--loop-delay', help = 'Loop iteration delay', default = '0')
def play(name: str, count: str, delay: str, loop_delay: str) -> None:
    '''
    Play a specific macro.
    '''
    
    with open(name + '.vomit', 'rb') as raw:
        events_list = pickle.load(raw)
    
    # Delay
    if delay and delay.isdigit():
        delay = int(delay)
    
    else: delay = 0
    
    print()
    for i in range(delay):
        print(f'\rStarting playing in \033[91m{delay - i: >4}', end = '\033[0m')
        time.sleep(1)
    
    t_size = os.get_terminal_size().columns
    
    print(f'\r\033[92m{"*** Playing ***": ^{t_size}}\033[0m')
    
    def stopper(event) -> None:
        return event == macro.key.f8
    
    def on_done() -> None:
        print(f'\r\033[92m{"*** End playing ***": ^{t_size}}\033[0m')
    
    runner = macro.Runner()
    runner.play(count = int(count),
                loop_delay = int(loop_delay),
                stopper = stopper,
                callback = on_done,
                events = events_list)

cli.add_command(record)

if __name__ == '__main__':
    cli()

# EOF