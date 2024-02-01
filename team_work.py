from agent_util import execute_task
from llm_util import beagle_7B, mistral_30B, chat_7B
from tasks import task_identify, task_collect, task_formula, task_selection, task_replace
from tools.calculator_tools import CalculatorTools
from tools.sec_tools import SECTools
from tools.string_tools import StringTools

target_10K = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"

list = execute_task(beagle_7B, [], task_identify)["output"]
formula = execute_task(mistral_30B, [], task_formula(list))["output"]
final_list = execute_task(mistral_30B, [], task_selection(list, formula))["output"]
final_list = StringTools.clean_items(final_list.split(','))
final_values = execute_task(chat_7B, [SECTools.extract_from_10k], task_collect(final_list, target_10K))["output"]
free_cash_flow = execute_task(mistral_30B, [CalculatorTools.numerical_conversion],
                              task_replace(final_values.__str__(), formula))["output"]
print(free_cash_flow)
print("Free cash flow is:", eval(free_cash_flow))
