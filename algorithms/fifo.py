def fifo(page_reference, frame_size):
    page_faults = 0
    frames = []
    process_steps = []
    
    for page in page_reference:
        step = {
            'page': page,
            'frames_before': frames.copy(),
            'page_fault': False,
            'frames_after': None
        }
        
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            step['page_fault'] = True
            page_faults += 1
        
        step['frames_after'] = frames.copy()
        process_steps.append(step)
    
    return page_faults, process_steps