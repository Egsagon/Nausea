import time
import pynput.keyboard

from pprint import pprint
from typing import Callable

key = pynput.keyboard.Key

class Runner:
    
    def __init__(self) -> None:
        '''
        Represents a runner.
        '''
        
        self.input = pynput.keyboard.Controller()
        self.output = pynput.keyboard.Listener(self.wrap_handle(1),
                                               self.wrap_handle(0))
        self.output.start()
    
    def wrap_handle(self, press: bool) -> Callable:
        
        def wrapper(event):
            self.handle(self, press, event)
        
        return wrapper
    
    def stop(self) -> None:
        '''
        Stop the runner.
        '''
        
        self.output.stop()
    
    def handle(self, press, event) -> None:
        '''
        Handle events.
        '''
        
        pass

    def record(self,
               stopper: Callable,
               on_event: Callable,
               callback: Callable) -> None:
        '''
        Start recording events.
        '''
        
        print('Recording...')
        
        def handle_stop() -> None:
            '''
            Stop recording and return events.
            '''
            
            # Reset handle
            self.handle = VOID
            
            # process
            callback(events)
        
        def handle_overwrite(self, event_type, event) -> None:
            '''
            Overwrite the runner handle.
            '''
            
            # Check for stop events
            if stopper(event):
                return handle_stop()
            
            # Process event
            event_time = round(time.time() - start, 5)
            
            if isinstance(event, pynput.keyboard.Key):
                event_repr = event.name
            
            else:
                event_repr = event.char
            
            event_type_repr = ('release', 'press')[event_type]
            
            processed = (event_time,
                         event_type,
                         event_type_repr,
                         event_repr,
                         event)
            
            # Check that event is not an echo
            if len(events):
                last_event = events[-1]
                
                if event_type == last_event[1] and event_repr == last_event[-2]:
                    
                    print('Bypassing echo:', processed)
                    return
            
            # Register event
            on_event(processed)
            events.append(processed)
        
        events = []
        start = time.time()
        
        # Overwrite
        self.handle = handle_overwrite

    def play(self,
             count: int | None,
             loop_delay: float,
             stopper: Callable,
             callback: Callable,
             events: list[tuple]) -> None:
        '''
        Play events.
        '''
        
        # Setup stopper
        def handle_overwrite(self, type, event):
            nonlocal stop
            
            if stopper(event):
                stop = True
        
        self.handle = handle_overwrite
        
        stop = False
        
        iterations = 0
        while not stop:
            
            # Check for stop
            iterations += 1
            if iterations > count:
                return callback()
            
            # Play once
            timeline = time.time()

            while events:
                event = events[0]
                event_time = event[0]
                
                if time.time() - timeline >= event_time:
                    # Execute event
                    
                    self._play_key(event)
                    events.pop(0)
        
            # Wait for loop delay
            time.sleep(loop_delay)
        
        # Send end signal
        return callback()

    def _play_key(self, event: tuple) -> None:
        '''
        Play one event. 
        '''
        
        print('[>]', event[2], event[3])
        
        # Press or release key
        getattr(self.input, event[2])(event[-1])

    @property
    def running(self) -> bool:
        '''
        Wether the runner is running.
        '''
        return self.output.is_alive()
    
    def block(self):
        
        while self.running:
            pass

def VOID(self, *args) -> None:
    '''
    Represents an empty handle.
    '''
    
    pass


if __name__ == '__main__':
    
    runner = Runner()
    
    def stopper(event):
        return event is pynput.keyboard.Key.esc
    
    def play_stop(event):
    
        stop = stopper(event)
        if stop: runner.stop()
        return stop
    
    def on_event(*args):
        print('[*] New entry:', args)
    
    def on_play_done():
        print('Done playing.')
        runner.stop()
    
    def on_done(events):
        print('Done. Event are:')
        pprint(events)
        
        print('Playing...')
        runner.play(1, 0, play_stop, on_play_done, events)
    
    runner.record(stopper, on_event, on_done)
    
    # Sample blocking stuff
    while runner.running:
        pass
    print('Runner thread stopped.')

# EOF