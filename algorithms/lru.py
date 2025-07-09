def lru(page_reference, frame_size):
    page_faults = 0
    frames = []
    page_index_map = {}  # Map to store the most recent index of each page
    process_steps = []
    
    for i, page in enumerate(page_reference):
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
                # Find the least recently used page
                lru_page = min(frames, key=lambda x: page_index_map[x])
                frames.remove(lru_page)
                frames.append(page)
            step['page_fault'] = True
            page_faults += 1
        
        # Update the most recent index of the current page
        page_index_map[page] = i
        
        step['frames_after'] = frames.copy()
        process_steps.append(step)
    
    return page_faults, process_steps