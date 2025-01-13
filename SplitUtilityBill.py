from pypdf import PdfReader

reader = PdfReader('D:/Users/Stephen/Documents/Real Estate/Duke_Energy_910100697321_12_11_24.pdf')

gas_count=0
electric_count=0
charges_count=0
first_gas_charge=""
second_gas_charge=""
first_electric_charge=""
second_electric_charge=""
total_amount_due=""
total_other_charges=""
total_taxes=""

for page in reader.pages:
    text = (page.extract_text())
    for line in text.split("\n"):
        find_date = "For service"
        if find_date in line:
            bill_date_range=line.replace("For service","")
            bill_date_range = bill_date_range.replace("STEPHEN RYBARCZYK", "").strip()
        find_total_gas_charges = "Current Gas Charges"
        if find_total_gas_charges in line:
            total_gas_charges=line.replace("Current Gas Charges","").strip()
            total_gas_charges = "$"+total_gas_charges
        find_total_electric_charges = "Current Electric Charges"
        if find_total_electric_charges in line:
            total_electric_charges = line.replace("Current Electric Charges", "").strip()
            total_electric_charges = "$" + total_electric_charges
        find_total_other_charges = "Total Other Charges and Credits"
        if find_total_other_charges in line:
            total_other_charges = line.replace("Total Other Charges and Credits", "").strip()
        find_total_taxes = "Total Taxes"
        if find_total_taxes in line:
            total_taxes = line.replace("Total Taxes", "").strip()
        find_total_amount_due = "Total Amount Due"
        if find_total_amount_due in line:
            total_amount_due = line[line.find("$"):].strip()
        find_total_gas_usage = "Gas (CCF)"
        if find_total_gas_usage in line:
            total_gas_usage = line.replace("Gas (CCF)", "").strip()
            total_gas_usage = total_gas_usage[:total_gas_usage.find(" ")].strip()
        find_first_gas_meter = "1297602"
        if find_first_gas_meter in line:
            first_gas_meter = line.replace("Current Gas usage for meter number ", "").strip()
        find_second_gas_meter = "1284594"
        if find_second_gas_meter in line:
            second_gas_meter = line.replace("Current Gas usage for meter number ", "").strip()
        find_gas_usage = "Gas Used"
        if find_gas_usage in line:
            if gas_count==0:
                first_gas_usage=line.replace("Gas Used ", "").strip()
                gas_count+=1
            elif gas_count == 1:
                second_gas_usage = line.replace("Gas Used ", "").strip()
                gas_count += 1

        find_total_electric_usage = "Electric (kWh)"
        if find_total_electric_usage in line:
            total_electric_usage = line.replace("Electric (kWh) ", "").strip()
            total_electric_usage = total_electric_usage[:total_electric_usage.find(" ")].strip()
        find_first_electric_meter = "320354640"
        if find_first_electric_meter in line:
            first_electric_meter = line.replace("Current electric usage for meter number ", "").strip()
        find_second_electric_meter = "320343403"
        if find_second_electric_meter in line:
            second_electric_meter = line.replace("Current electric usage for meter number ", "").strip()
        find_electric_usage = "Energy Used"
        if find_electric_usage in line:
            if electric_count==0:
                first_electric_usage=line.replace("Energy Used ", "").strip()
                electric_count+=1
            elif electric_count == 1:
                second_electric_usage = line.replace("Energy Used ", "").strip()
                electric_count += 1
        find_charges = "Total Current Charges "
        if find_charges in line:
            if charges_count==0:
                first_gas_charge=line[line.find("$"):].strip()
                charges_count+=1
            elif charges_count == 1:
                second_gas_charge=line[line.find("$"):].strip()
                charges_count+=1
            elif charges_count == 2:
                first_electric_charge=line[line.find("$"):].strip()
                charges_count+=1
            elif charges_count == 3:
                second_electric_charge=line[line.find("$"):].strip()
                charges_count+=1

check_total=round((
            float(first_gas_charge[1:].strip())+float(second_gas_charge[1:].strip())+float(first_electric_charge[1:].strip())+
            +float(second_electric_charge[1:].strip())+float(total_other_charges[1:].strip())+float(total_taxes[1:].strip())
            ),2)
gas_electric_charges=float(total_gas_charges[1:].strip())+float(total_electric_charges[1:].strip())
unit_a_gas_tax=round(float(second_gas_charge[1:].strip())/gas_electric_charges*float(total_taxes[1:].strip()),2)
unit_a_electric_tax=round(float(second_electric_charge[1:].strip())/gas_electric_charges*float(total_taxes[1:].strip()),2)
unit_b_gas_tax=round(float(first_gas_charge[1:].strip())/gas_electric_charges*float(total_taxes[1:].strip()),2)
unit_b_electric_tax=round(float(first_electric_charge[1:].strip())/gas_electric_charges*float(total_taxes[1:].strip()),2)

unit_a_gas_total=round(float(second_gas_charge[1:].strip())+unit_a_gas_tax,2)
unit_a_electric_total=round(float(second_electric_charge[1:].strip())+unit_a_electric_tax,2)
unit_b_gas_total=round(float(first_gas_charge[1:].strip())+unit_b_gas_tax,2)
unit_b_electric_total=round(float(first_electric_charge[1:].strip())+unit_b_electric_tax,2)

unit_a_total=round(unit_a_gas_total+unit_a_electric_total,2)
unit_b_total=round(unit_b_gas_total+unit_b_electric_total,2)

message_content="Unit A\nGas Charges: $"+str(unit_a_gas_total)+"\nElectric Charges: $"+str(unit_a_electric_total)+"\nTotal Charges: $"+str(unit_a_total)
message_content=message_content+"\nUnit B\nGas Charges: $"+str(unit_b_gas_total)+"\nElectric Charges: $"+str(unit_b_electric_total)+"\nTotal Charges: $"+str(unit_b_total)+"\n"
if float(total_other_charges[1:].strip())>0:
    message_content=message_content+"\nOther charges of "+total_other_charges+" are present.\n"
if check_total==float(total_amount_due[1:].strip()):
    message_content=message_content+"\nTotals match."
else:
    message_content=message_content+"\nTotals don't match."
print (message_content)

