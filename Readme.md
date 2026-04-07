
# This repo consist of my python learnings

# Asyncio

This section contains notes on **Python asyncio**, including coroutines, tasks, futures, and event loop behavior.

---

## Working

- `asyncio` enables **concurrent execution** using a **single thread**
- It uses an **event loop** to manage execution
- Tasks don’t run in parallel (like threads), but they **interleave execution**

---

## Event Loop

- The **event loop** is the heart of asyncio
- It:
  - Schedules coroutines
  - Switches execution when `await` is encountered
  - Handles I/O efficiently

```python
asyncio.run(main())
```

---

## Coroutines

- Defined using `async def`
- Must be **awaited** to execute

```python
async def fetch(delay):
    await asyncio.sleep(delay)
    return "hi"
```

### Important

```python
task = fetch(2)
```

- This does **NOT run the coroutine**
- It only creates a coroutine object

```python
await task
```

- This actually executes it

---

## Await

- `await` pauses the current coroutine
- Gives control back to the event loop

```python
await asyncio.sleep(2)
```

 During this time, other tasks can run

---

## Tasks

- Used to run coroutines **concurrently**

```python
asyncio.create_task(fetch(2))
```

### important

- Task starts **immediately**
- Runs in background
- Doesn’t block execution

---

## Concurrent Execution

```python
task1 = asyncio.create_task(fetch(2))
task2 = asyncio.create_task(fetch(1))

await task1
await task2
```

Both run **concurrently**, not sequentially

---

## asyncio.gather()

- Runs multiple coroutines concurrently

```python
results = await asyncio.gather(
    fetch(2),
    fetch(1)
)
```

- Waits for **all to complete**
- Returns results in order

---

## Futures

- Low-level object representing a value that will be available later

```python
future = loop.create_future()
```

### Example Flow

```python
async def producer(future):
    await asyncio.sleep(2)
    future.set_result("important value")
```

```python
result = await future
```

`await future` resumes **as soon as result is set**

---



### Future vs Normal Await

- `await coroutine` → waits for full execution
- `await future` → resumes when `set_result()` is called

---

## Execution Flow Insight

```python
asyncio.create_task(producer(future))

await asyncio.sleep(10)
result = await future
```

### Important Observation:

- Even if producer continues doing work after `set_result`
- `await future` resumes **immediately after result is set**

---



"Asyncio is a single worker who switches tasks whenever it has to wait"

---

## When to Use Asyncio

- Network requests
- Web scraping
- APIs
- WebSockets
- I/O-bound tasks

---

## When NOT to Use

- CPU-heavy tasks (use multiprocessing instead)

---

## Final Summary

- `async def` → defines coroutine  
- `await` → pauses and yields control  
- `create_task()` → runs concurrently  
- `gather()` → run multiple tasks  
- `future` → manual control over result  

- Coroutines don’t run unless awaited or scheduled  
- Event loop manages everything  
- Futures can return early even if task continues  
- Asyncio is about **efficient waiting**, not speed  

---
