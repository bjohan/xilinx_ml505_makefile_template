from functions.function_ids import functionId
import functions.debug_core
functionName = {v: k for k, v in functionId.items()}
functionMap = {functionId['debug_core']:functions.debug_core.DebugCore}
