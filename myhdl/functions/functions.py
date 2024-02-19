from functions.function_ids import functionId
import functions.debug_core
import functions.mdio_interface
functionName = {v: k for k, v in functionId.items()}
functionMap = {
                functionId['debug_core']:functions.debug_core.DebugCore,
                functionId['mdio_interface']:functions.mdio_interface.MdioInterface,
}
