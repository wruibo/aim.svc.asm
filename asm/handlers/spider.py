from .. import access, handler, protocol, spiders, error


class EnableHandler(handler.Handler):
    @access.protect
    def get(self):
        """
            enable spider
        :return:
        """
        # get parameters
        id = self.get_argument('spider', None)

        # process request
        spiders.manager.enable(id)

        return self.write(protocol.success())

    post = get


class DisableHandler(handler.Handler):
    @access.protect
    def get(self):
        """
            disable spider
        :return:
        """
        # get parameters
        id = self.get_argument('spider', None)

        # process request
        spiders.manager.disable(id)

        return self.write(protocol.success())

    post = get


class StatusHandler(handler.Handler):
    @access.protect
    def get(self):
        """
            get status
        :return:
        """
        # get parameters
        id = self.get_argument('spider', None)

        # process request
        result = spiders.manager.status(id)

        return self.write(protocol.success(data=result))

    post = get
