def optimal(page_reference, frame_size):
    page_faults = 0
    frames = []
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
                future_pages = [page_reference[j] for j in range(i + 1, len(page_reference))]
                next_use = {p: float('inf') for p in frames}
                for p in frames:
                    if p not in future_pages:
                        next_use[p] = float('inf')
                    else:
                        next_use[p] = future_pages.index(p)
                victim = max(next_use, key=next_use.get)
                frames.remove(victim)
                frames.append(page)
            step['page_fault'] = True
            page_faults += 1
        
        step['frames_after'] = frames.copy()
        process_steps.append(step)
    
    return page_faults, process_steps