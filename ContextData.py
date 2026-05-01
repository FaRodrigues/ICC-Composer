class CustomerData:
    def __init__(self):
        self.customer_context = {'customerName': "",
                                 'customerShortName': "",
                                 'customerNameAbrev': "",
                                 'customerAddress': "",
                                 'customerCompleteAddress': ""
                                 }

    def getCustomerContext(self):
        return self.customer_context

    def setCustomerName(self, cn):
        self.customer_context['customerName'] = cn

    def setCustomerShortName(self, csn):
        self.customer_context['customerShortName'] = csn

    def setCustomerNameAbrev(self, cnab):
        self.customer_context['customerNameAbrev'] = cnab

    def setCustomerAddress(self, ca):
        self.customer_context['customerAddress'] = ca

    def setCustomerCompleteAddress(self, cca):
        self.customer_context['customerCompleteAddress'] = cca


class CalibrationLaboratoryData:
    def __init__(self):
        self.calibrationLaboratory_context = {'calibrationLaboratoryName': "",
                               'calibrationLaboratoryShortName': "",
                               'calibrationLaboratoryNameAbrev': "",
                               'calibrationLaboratoryAddress': "",
                               'calibrationLaboratoryCompleteAddress': ""
                               }

    def getCalibrationLaboratoryContext(self):
        return self.calibrationLaboratory_context

    def setCalibrationLaboratoryName(self, cn):
        self.calibrationLaboratory_context['calibrationLaboratoryName'] = cn

    def setCalibrationLaboratoryShortName(self, csn):
        self.calibrationLaboratory_context['calibrationLaboratoryShortName'] = csn

    def setCalibrationLaboratoryNameAbrev(self, cnab):
        self.calibrationLaboratory_context['calibrationLaboratoryNameAbrev'] = cnab

    def setCalibrationLaboratoryAddress(self, ca):
        self.calibrationLaboratory_context['calibrationLaboratoryAddress'] = ca

    def setCalibrationLaboratoryCompleteAddress(self, cca):
        self.calibrationLaboratory_context['calibrationLaboratoryCompleteAddress'] = cca
